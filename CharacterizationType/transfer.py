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

class NANOBIO_TransferCharacterization():
    def __init__(self, measuringInstrument,tp, datalogger):
        ###---------------- MEASUREMENT PARAMETERS ----------------###
        
        self.Vds = tp.Vds
        self.doubleSweep = tp.doubleSweep
        #for single sweep
        self.Vgs_Start = tp.Vgs_Start
        self.Vgs_end = tp.Vgs_end
        self.sweepDelay = tp.sweepDelay
        # for double sweep
        self.startV = tp.startV
        self.Vgs_maxV =   tp.Vgs_maxV
        self.Vgs_minV = tp.Vgs_minV
        self.Vgs_step = tp.Vgs_step
        self.id_limit_ms = tp.id_limit_ms
        self.ig_limit_ms = tp.ig_limit_ms

        self.measurementRange = 'auto'
        self.Sourcemode = 'DC_V'
        
        if tp.ins_u2722a:
            self.gate = 1
            self.drain = 2
        elif tp.ins_k2636 :
            self.gate = 'smua'
            self.drain = 'smub'
        else:
            self.gate = 'smua'
            self.drain = 'smub'

        self.number_of_transfer_meas = tp.number_of_transfer_meas


        ##############################################################
        
        self.timestep = []
        self.Id = []
        self.Ig = []
        self.VgsBuffer = []
        self.xdata = []
        self.idydata = []
        self.igydata = []
        self.timestamp = []
        self.dl = datalogger

        ########### OBJECTS TO PLOT THE DATA #################
        self.qapp = pg.mkQApp()
        self.win = pg.GraphicsWindow()
        
        self.idplot = self.win.addPlot(row=0, col=1)  
        self.idcurve = self.idplot.plot()
        self.idcurve.setPen('b')

        self.igplot = self.win.addPlot(row=0, col=2)  
        self.igcurve = self.igplot.plot()
        self.igcurve.setPen('r')

        self.measuringinstrument = measuringInstrument     
        self.measurementDone = False
        self.DataSaved = False
        self.clean_exit_signal = False
        self.dataAquisition_thread = True
        self.measurement_finished_wo_interuption = False

    def startMeasurement(self):
        self.dataAquisition_thread = FuncThread(self.executeDataAquisition)
        self.dataAquisition_thread.start()
        
        try:
            while ( (self.measurementDone != True) and ( self.win.isVisible() == True) ):
                self.idcurve.setData(self.xdata, self.idydata)
                self.igcurve.setData(self.xdata, self.igydata)
                self.qapp.processEvents()
            self.CleanExit()
            
        except:
            self.CleanExit()
            print('issue in plotting')
            raise Exception
        
    def CleanExit(self):
        self.clean_exit_signal = True
        if (self.measurement_finished_wo_interuption == False):
            self.dataAquisition_thread.join()
        self.win.close()
        if self.DataSaved != True:
            self.dl.saveTransfer(self.Id, self.Ig, self.VdsBuffer, self.VgsBuffer, self.timestamp)
            self.DataSaved = True
        self.measuringinstrument.channeloff(self.gate)
        self.measuringinstrument.channeloff(self.drain)
        self.measurementDone = True

    def executeDataAquisition(self):
        self.measuringinstrument.Configure( self.measurementRange,  self.Sourcemode,  self.gate, self.ig_limit_ms)
        self.measuringinstrument.Configure( self.measurementRange,  self.Sourcemode,  self.drain, self.id_limit_ms)
        set_range_counter = 5
        present_range_Ig = 10e-6
        present_range_Id  = 10e-6
        self.measuringinstrument.channelon( self.gate)
        self.measuringinstrument.channelon( self.drain)
        self.measuringinstrument.setVoltage(self.drain, self.Vds)
        self.measuringinstrument.measureId_VgsStep( self.gate,  self.drain, 0)
        
        self.dl.WriteMeasurementSettings(self.getMeasurementSettings())

        # if self.doubleSweep == True:
        self.Vgs = GetDoubleSweep( self.startV, self.Vgs_maxV,  self.Vgs_minV,  self.Vgs_step, self.number_of_transfer_meas)
        rows_of_measurement_data =  np.zeros(len(self.Vgs)) 
        self.Id = np.zeros(len(self.Vgs)) 
        self.Ig = np.zeros(len(self.Vgs))  
        self.VdsBuffer = np.zeros(len(self.Vgs))   
        self.timestamp = np.zeros(len(self.Vgs))  
        self.VgsBuffer = np.zeros(len(self.Vgs)) 
        # else:
        #     Vgs = GetSweepVoltage( self.Vgs_Start,  self.Vgs_end,  self.Vgs_step)
        measurementTime = 0
    
        for vgs_index in range(len(self.Vgs)):
            if self.clean_exit_signal:
                return
            t0 = time.time()
            measured_Id, measured_Ig = self.measuringinstrument.measureId_Ig_VgsStep( self.gate, self.drain,self.Vgs[vgs_index], self.sweepDelay)
            dt = time.time()-t0
            measurementTime += dt
            set_range_counter -= 1
            # set_range_counter = 1
            ##########  FIX THE MEASUREMENT RANGE
            if set_range_counter <= 0:
                set_range_counter = 5
                present_range_Ig = self.measuringinstrument.SetRange(self.Sourcemode, measured_Ig, present_range_Ig, self.gate)
                present_range_Id = self.measuringinstrument.SetRange(self.Sourcemode, measured_Id, present_range_Id, self.drain)
            time.sleep(self.sweepDelay)  

            self.Id[vgs_index] = measured_Id
            self.Ig[vgs_index] = measured_Ig
            self.VgsBuffer[vgs_index] = self.Vgs[vgs_index]
            self.VdsBuffer[vgs_index] = self.Vds
            self.timestamp[vgs_index] = measurementTime
            self.xdata.append( self.Vgs[vgs_index])
            self.idydata.append(measured_Id)
            self.igydata.append(measured_Ig)
        self.measurementDone = True
        self.measurement_finished_wo_interuption = True    
        return


    def getMeasurementSettings(self):
        settings =  (
                     '\n# ' + self.dl.measCond
                    +'\n#  Vds = '+ str(self.Vds)
                    +'\n#  Vgs_start = ' + str(self.startV )
                    +'\n#  Vgs_max = ' + str(self.Vgs_maxV) 
                    +'\n#  Vgs_min  = ' + str(self.Vgs_minV )
                    +'\n#  Vgs_step  = ' + str(self.Vgs_step)
                    +'\n#  measurementRange = ' + str(self.measurementRange) 
                    +'\n#  Sourcemode  = ' + str(self.Sourcemode )
                    +'\n#  gate  = ' + str(self.gate )
                    +'\n#  drain  = ' + str(self.drain) 
                    +'\n#  sweepDelay  = ' + str(self.sweepDelay)
        )
        return settings 