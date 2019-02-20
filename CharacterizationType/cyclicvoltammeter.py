import numpy as np
import pyqtgraph as pg
import threading
import time
from Utils.converter import *


from DataLogger.datalogger import datalogger
from DataProcessing.processData import processData
import arrow
from Utils.FuncThread import FuncThread
from Utils.sweepUtils import *

class NanoBIO_CVCharacterizer():
    def __init__(self, measuringInstrument, cvp, datalogger):
       
        ###---------------- MEASUREMENT PARAMETERS ----------------### 
        self.startV = cvp.startV
        self.endV = cvp.endV
        self.minV = cvp.minV
        self.scan_rate = cvp.scan_rate
        self.step_size = cvp.step_size
        self.cycles = cvp.cycles
        self.channel = 'smua'
        self.measurementRange = 'auto'
        self.Sourcemode = 'DC_V'   
        self.I_limit = cvp.I_limit   
        ##############################################################
        self.timestep = []
        self.I = []
        self.V = []
        self.xdata = []
        self.ydata = []
        self.timestamp = []
        self.dl = datalogger
        
        ################ OBJECTS TO PLOT THE DATA ################
        self.qapp = pg.mkQApp()
        self.win = pg.GraphicsWindow()
        self.plot1 = self.win.addPlot()  
        self.curve = self.plot1.plot()
        self.curve.setPen(None)
        self.curve.setSymbol('o')
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
            self.dl.save_cyclic_voltammetery(self.V, self.I, self.timestamp)
            self.DataSaved = True
        self.measurementDone = True
        self.measuringinstrument.TurnoffChannels()

    def executeDataAquisition(self):
        self.measuringinstrument.SetupVoltammeter(self.measurementRange, self.Sourcemode, self.channel, self.I_limit)
        set_range_counter = 5
        present_range_I = 1e-03
        self.dl.WriteMeasurementSettings(self.getMeasurementSettings())
        measurementTime = 0
        volt_array  = GetDoubleSweep(self.startV,self.endV,self.minV, self.step_size, self.cycles)
        step_delay = self.step_size / self.scan_rate  # in seconds

        t0 = time.time()
        for single_step in volt_array:
            if self.clean_exit_signal:
                return
            I = self.measuringinstrument.measureI_VStep(self.channel, single_step, step_delay)
            dt = time.time()-t0
            measurementTime += dt 
            set_range_counter -= 1
            ##########  FIX THE MEASUREMENT RANGE
            if set_range_counter <= 0:
                set_range_counter = 5
                present_range_I = self.measuringinstrument.SetRange(self.Sourcemode, I, present_range_I, self.channel)
            ####################  save the data ###############
            self.I.append(I)
            self.V.append(single_step)
            self.timestamp.append(measurementTime)                
            self.xdata = self.V
            self.ydata = self.I

        self.measurementDone = True
        self.measurement_finished_wo_interuption = True
        return

    def getMeasurementSettings(self ):
        settings =  (           
                     '\n#  ' + self.dl.measCond
                    +'\n#StartV = '+ str(self.startV)
                    +'\n#MaxV = ' + str(self.endV )
                    +'\n#MinV = ' + str(self.minV )
                    +'\n#Scan rate = ' + str(self.scan_rate ) + r'V/s'
                    +'\n#Step size  = ' + str(self.step_size ) + r'V'
                    +'\n#Cycles = ' + str(self.cycles) 
        )
        return settings
    