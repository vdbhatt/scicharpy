import numpy as np
import pyqtgraph as pg
import threading
import time
from Instruments.K2636_GPIB import * 
from Utils.sweepUtils import *

from DataLogger.datalogger import datalogger
from DataProcessing.processData import processData
import arrow 
from Utils.FuncThread import FuncThread

class NANOBIO_OnlineMeas():
    def __init__(self, measuringInstrument, sp, datalogger):
        ###---------------- MEASUREMENT PARAMETERS ----------------###
        self.Vds = sp.Vds
        self.Vgs = sp.Vgs
        self.Time = sp.Time
        self.unlimited_meas = sp.unlim_meas
        self.sweep_delay_ms = sp.sweep_delay_ms
        self.type = sp.type
        self.solution = sp.solution
        self.id_limit_ms = sp.id_limit_ms
        self.ig_limit_ms = sp.ig_limit_ms
        self.keep_vg_on = sp.keep_vg
        self.keep_vd_on = sp.keep_vd 
        self.vg_ac = sp.vg_ac
        self.vg_dc = sp.vg_dc
        
        
        self.measurementRange = 'auto'
        self.Sourcemode = 'DC_V'
        
        if sp.ins_u2722a:
            self.gate = 1
            self.drain = 2
        elif sp.ins_k2636 :
            self.gate = 'smua'
            self.drain = 'smub'
        else:
            self.gate = 'smua'
            self.drain = 'smub'
            
        ########################## CONTAINERS TO HOLD THE MEASUREMENT & PLOTTING DATA #######################
        self.timestep = []
        self.Id = []
        self.Ig = []
        self.xdata = []
        self.idydata = []
        self.igydata = []
        self.timestamp = []
        self.dl = datalogger 

        ################# OBJECTS TO PLOT THE DATA ######################
        self.qapp = pg.mkQApp()
        self.win = pg.GraphicsWindow()
        
        self.idplot = self.win.addPlot()  
        self.idcurve = self.idplot.plot()
        self.idcurve.setPen('g')

        self.igplot = self.win.addPlot()  
        self.igcurve = self.igplot.plot()
        self.igcurve.setPen('r')

        self.measuringinstrument = measuringInstrument     
        self.measurementDone = False
        self.measurementPause = False
        self.measurementContinue = False
        self.updateMeasValues = False
        self.DataSaved = False
        self.clean_exit_signal = False
        self.dataAquistion_thread = True
        self.measurment_finished_without_interuption = False

    def startMeasurement(self):
        '''
        executeDataAquisition is a new process that each time when a new value was added to  
        '''
        self.dataAquistion_thread = FuncThread(self.executeDataAquisition)
        self.dataAquistion_thread.start()

        while ((self.measurementDone != True) and (self.win.isVisible()==True)):
            try:
                self.idcurve.setData(self.xdata, self.idydata)
                self.igcurve.setData(self.xdata, self.igydata)
                self.qapp.processEvents()
            except:
                pass
        self.CleanExit()

    def CleanExit(self):
        self.clean_exit_signal = True
        if(self.measurment_finished_without_interuption == False):
            self.dataAquistion_thread.join()
        self.win.close()
        if self.DataSaved != True:
            self.dl.saveOnline_Measurement(self.Id, self.Ig, self.Vds, self.Vgs , self.timestamp)
            self.DataSaved = True
        if self.keep_vg_on == True and self.keep_vd_on == True:
            self.measuringinstrument.setVoltage(self.gate, 0)
            self.measuringinstrument.setVoltage(self.drain, 0)
        elif self.keep_vg_on == True:
            self.measuringinstrument.setVoltage(self.gate, 0)
            self.measuringinstrument.channeloff(self.drain)
        elif self.keep_vd_on == True:
            self.measuringinstrument.setVoltage(self.drain, 0)
            self.measuringinstrument.channeloff(self.gate)
        else:
            self.measuringinstrument.channeloff(self.gate)
            self.measuringinstrument.channeloff(self.drain)
        self.measurementDone = True

    def rampGate(self):
        self.measuringinstrument.measureId_VgsStep(self.gate, self.drain, 0.2*self.Vgs)
        time.sleep(0.1)
        self.measuringinstrument.measureId_VgsStep(self.gate, self.drain, 0.4*self.Vgs)
        time.sleep(0.1)
        self.measuringinstrument.measureId_VgsStep(self.gate, self.drain, 0.6*self.Vgs)
        time.sleep(0.1)
        self.measuringinstrument.measureId_VgsStep(self.gate, self.drain, 0.8*self.Vgs)
        time.sleep(0.1)

    def executeDataAquisition(self):
        self.measuringinstrument.Configure( self.measurementRange,  self.Sourcemode,  self.gate, self.ig_limit_ms)
        self.measuringinstrument.Configure( self.measurementRange,  self.Sourcemode,  self.drain, self.id_limit_ms)
        set_range_counter = 5
        present_range_Ig = 1e-3
        present_range_Id  = 1e-3
        self.measuringinstrument.channelon( self.gate)
        self.measuringinstrument.channelon( self.drain)
        self.measuringinstrument.setVoltage(self.drain, self.Vds)
        self.rampGate()
        measurementTime = 0
        
        self.dl.WriteMeasurementSettings(self.getMeasurementSettings())
        counter = 0
        while (measurementTime < self.Time or self.unlimited_meas == True) :
            if self.clean_exit_signal:
                return
            while ((self.measurementPause) and (self.measurementContinue != True)):
                t0 = time.time()
                self.measuringinstrument.setVoltage(self.gate, 0)
                self.measuringinstrument.setVoltage(self.drain, 0)
                dt = time.time()-t0
                measurementTime += dt
                self.Id.append(0)
                self.Ig.append(0)
                self.timestamp.append(measurementTime) 
                self.xdata = self.timestamp
                self.idydata = self.Id
                self.igydata = self.Ig    
            
            if self.measurementContinue:
                # self.dl.saveOnline_Measurement(self.Id, self.Ig, self.Vds, self. Vgs, self.timestep)
                self.measuringinstrument.setVoltage(self.drain, self.Vds)
                self.rampGate()
                self.measurementContinue = False
                self.measurementPause = False
            else:
                pass

            t0 = time.time()
            if self.vg_ac:
                counter = counter + 1
                vgs_sin = self.Vgs*np.sin(counter*np.pi/10)
                # print(np.pi*2*5*measurementTime, vgs_sin)
                measured_Id, measured_Ig = self.measuringinstrument.measureId_Ig_VgsStep( self.gate, self.drain, vgs_sin, self.sweep_delay_ms)
            else:
                measured_Id, measured_Ig = self.measuringinstrument.measureId_Ig_VgsStep( self.gate, self.drain, self.Vgs, self.sweep_delay_ms)

            dt = time.time()-t0
            measurementTime += dt
            set_range_counter -= 1

            ##########  FIX THE MEASUREMENT RANGE
            if set_range_counter <= 0:
                set_range_counter = 5
                present_range_Ig = self.measuringinstrument.SetRange(self.Sourcemode, measured_Ig, present_range_Ig, self.gate)
                present_range_Id = self.measuringinstrument.SetRange(self.Sourcemode,  measured_Id, present_range_Id, self.drain)
            ##########  UPDATE THE DATA CONTAINERS 
            self.Id.append(measured_Id)
            self.Ig.append(measured_Ig)
            self.timestamp.append(measurementTime) 
            self.xdata = self.timestamp
            self.idydata = self.Id
            self.igydata = self.Ig
            ##############  SAVE THE DATA USING THE LOGGING OBJECT ######################
            # self.dl.append_OnlineData(measured_Id, measured_Ig, self.Vds, self.Vgs , measurementTime)
        self.measurementDone = True
        measurment_finished_without_interuption = True
        return
    
    def updateValues(self,sp):
        self.Vds = sp.Vds
        self.Vgs = sp.Vgs
        self.Time = sp.Time
        self.unlimited_meas = sp.unlim_meas
        self.sweep_delay_ms = sp.sweep_delay_ms
        self.type = sp.type
        self.solution = sp.solution
        self.id_limit_ms = sp.id_limit_ms
        self.ig_limit_ms = sp.ig_limit_ms
        self.keep_vg_on = sp.keep_vg
        self.keep_vd_on = sp.keep_vd 
        self.vg_ac = sp.vg_ac
        self.vg_dc = sp.vg_dc
        self.updateMeasValues = False

    def getMeasurementSettings(self):
        settings =  ('\n# solution = '+ str(self.type) + r' ' + str(self.solution)
                    +'\n#  Vds = '+ str(self.Vds)
                    +'\n#  Vgs  = ' + str(self.Vgs )
                    +'\n#  Time = ' + str(self.Time)
                    +'\n#  measurementRange = ' + str(self.measurementRange) 
                    +'\n#  Sourcemode  = ' + str(self.Sourcemode )
                    +'\n#  gate  = ' + str(self.gate )
                    +'\n#  drain  = ' + str(self.drain) 
                    +'\n#  sweep_delay_ms  = ' + str(self.sweep_delay_ms)
                    +'\n#  ' + self.dl.measCond
        )
        return settings 
