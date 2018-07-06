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

class NANOBIO_ChannelResistance():
    def __init__(self, measuringInstrument,rp, datalogger):
        ###---------------- MEASUREMENT PARAMETERS ----------------### 
       
        self.Vds_Start = rp.Vds_Start
        self.Vds_max = rp.Vds_max
        self.Vds_min = rp.Vds_min
        self.Vds_step = rp.Vds_step
    
        self.sweepDelay = rp.sweepDelay
        self.number_of_res_meas = rp.number_of_res_meas
        self.id_limit_ms = rp.id_limit_ms

        self.measurementRange = 'auto'
        self.Sourcemode = 'DC_V'
        self.drain = 'smub'

        ##############################################################
        self.timestep = []
        self.Id = []
        self.VdsBuffer = []
        self.xdata = []
        self.ydata = []
        self.timestamp = []
        self.dl = datalogger
        
        ################ OBJECTS TO PLOT THE DATA ################
        self.qapp = pg.mkQApp()
        self.win = pg.GraphicsWindow()
        self.plot1 = self.win.addPlot()  
        self.curve = self.plot1.plot()
        self.curve.setPen('g')
        self.measuringinstrument = measuringInstrument    
        self.measurementDone = False
        self.DataSaved = False
        self.clean_exit_signal = False
        self.dataAquistion_thread = True
        self.measurement_finished_wo_interuption = False
 
    def startMeasurement(self):
        self.dataAquistion_thread = FuncThread(self.executeDataAquisition)
        self.dataAquistion_thread.start()
        
        try:
            while ((self.measurementDone != True) and (self.win.isVisible()==True)): 
                self.curve.setData(self.xdata, self.ydata)
                self.qapp.processEvents()
            self.CleanExit()
        except:
            self.CleanExit()
            print("issue in plotting")
            raise Exception

    def CleanExit(self):
        self.clean_exit_signal = True
        if (self.measurement_finished_wo_interuption == False):
            self.dataAquistion_thread.join()
        self.win.close()
        if self.DataSaved != True:
            self.dl.saveResistance(self.Id, self.VdsBuffer, self.timestamp)
            self.DataSaved = True
        self.measuringinstrument.channeloff(self.drain)
        self.measurementDone = True

    def executeDataAquisition(self):
        self.measuringinstrument.Configure(self.measurementRange, self.Sourcemode, self.drain, self.id_limit_ms)
        set_range_counter = 5
        present_range_Id = 1e-03
        self.measuringinstrument.channelon( self.drain)
        
        self.dl.WriteMeasurementSettings(self.getMeasurementSettings())
        
        Vds = GetDoubleSweep (self.Vds_Start, self.Vds_max, self.Vds_min, self.Vds_step, self.number_of_res_meas)
        
        measurementTime = 0
           
        for vds_step in Vds:
            if self.clean_exit_signal:
                return
            t0 = time.time()
            measured_Id = self.measuringinstrument.measureId_VdsStep( self.drain,  vds_step)
            dt = time.time()-t0
            measurementTime += dt 
            set_range_counter -= 1
            ##########  FIX THE MEASUREMENT RANGE
            if set_range_counter <= 0:
                set_range_counter = 5
                present_range_Id = self.measuringinstrument.SetRange( measured_Id, present_range_Id, self.drain)
            time.sleep(self.sweepDelay)       
            
            self.Id.append(measured_Id)
            self.VdsBuffer.append(vds_step)
            self.timestamp.append(measurementTime)                
            self.xdata = self.VdsBuffer
            self.ydata = self.Id
        self.measurementDone = True
        self.measurement_finished_wo_interuption = True
        return

        

    def getMeasurementSettings(self ):
        settings =  (           
                     '\n#  ' + self.dl.measCond
                    +'\n#Vds_Start = '+ str(self.Vds_Start)
                    +'\n#Vds_max = ' + str(self.Vds_max )
                    +'\n#Vds_min = ' + str(self.Vds_min )
                    +'\n#Vds_step  = ' + str(self.Vds_step )
                    +'\n#measurementRange = ' + str(self.measurementRange) 
                    +'\n#Sourcemode  = ' + str(self.Sourcemode )
                    +'\n#sweepDelay  = ' + str(self.sweepDelay)
        )
        return settings
