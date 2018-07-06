import numpy as np
import pyqtgraph as pg
import threading
import time
from Instruments.Fake_K2636_GPIB import * 
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
        self.sweep_delay_ms = sp.sweep_delay_ms
        self.type = sp.type
        self.solution = sp.solution
        self.id_limit_ms = sp.id_limit_ms
        self.ig_limit_ms = sp.ig_limit_ms
        
        self.measurementRange = 'auto'
        self.Sourcemode = 'DC_V'
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
            self.idcurve.setData(self.xdata, self.idydata)
            self.igcurve.setData(self.xdata, self.igydata)
            self.qapp.processEvents()
        self.CleanExit()

    def CleanExit(self):
        self.clean_exit_signal = True
        if(self.measurment_finished_without_interuption == False):
            self.dataAquistion_thread.join()
        self.win.close()
        if self.DataSaved != True:
            self.dl.saveOnline_Measurement(self.Id, self.Ig, self.Vds, self.Vgs , self.timestamp)
            self.DataSaved = True
        self.measuringinstrument.channeloff(self.gate)
        self.measuringinstrument.channeloff(self.drain)
        self.measurementDone = True

    def executeDataAquisition(self):
        self.measuringinstrument.Configure( self.measurementRange,  self.Sourcemode,  self.gate, self.ig_limit_ms)
        self.measuringinstrument.Configure( self.measurementRange,  self.Sourcemode,  self.drain, self.id_limit_ms)
        set_range_counter = 5
        present_range_Ig = 1e-3
        present_range_Id  = 1e-3
        self.measuringinstrument.channelon( self.gate)
        self.measuringinstrument.channelon( self.drain)
        self.measuringinstrument.setVoltage(self.drain, self.Vds)
        self.measuringinstrument.measureId_VgsStep( self.gate,  self.drain, 0)
        measurementTime = 0
        
        self.dl.WriteMeasurementSettings(self.getMeasurementSettings())
        
        while measurementTime < self.Time:
            if self.clean_exit_signal:
                return
            t0 = time.time()
            measured_Id, measured_Ig = self.measuringinstrument.measureId_Ig_VgsStep( self.gate, self.drain,  self.Vgs, self.sweep_delay_ms)
            dt = time.time()-t0
            measurementTime += dt
            set_range_counter -= 1

            ##########  FIX THE MEASUREMENT RANGE
            if set_range_counter <= 0:
                set_range_counter = 5
                present_range_Ig = self.measuringinstrument.SetRange( measured_Ig, present_range_Ig, self.gate)
                present_range_Id = self.measuringinstrument.SetRange( measured_Id, present_range_Id, self.drain)
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
