import numpy as np
import pyqtgraph as pg
import threading
import time
import arrow

from Utils.converter import *
from DataLogger.datalogger import datalogger
from DataProcessing.processData import processData
from Utils.FuncThread import FuncThread
from Utils.sweepUtils import *

class NanoBIO_PotentialCharacterizer():
    def __init__(self, measuringInstrument, pp, datalogger):
       
        ###---------------- MEASUREMENT PARAMETERS ----------------### 
        self.measurementDelay = pp.measurementDelay / 1000.0 # convert it to seconds 
        self.measurementDuration = pp.measurementDuration*1000 # convert it to ms
        self.measurementRange = 'auto'
        self.Sourcemode = 'DC_V'   
        ##############################################################
        self.timestep = []
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
        self.curve.setPen('g')
        #self.curve.setSymbol('o')
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
            self.DataSaved = self.dl.save_potential_measurement(self.V, self.timestamp)
        self.measurementDone = True
        self.measuringinstrument.TurnoffChannels()

    def executeDataAquisition(self):
        self.measuringinstrument.SetupPotentiostat()
        self.dl.WriteMeasurementSettings(self.getMeasurementSettings())
        measurementTime = 0

        t0 = time.time()

        while(measurementTime < self.measurementDuration):
            if self.clean_exit_signal:
                return
            V = self.measuringinstrument.GetV_PotentiostatMode(self.measurementDelay)
            dt = time.time()-t0
            measurementTime += dt 
            ####################  save the data ###############
            self.V.append(V)
            self.timestamp.append(measurementTime)      
            
            self.xdata = self.timestamp 
            self.ydata = self.V

        self.measurementDone = True
        self.measurement_finished_wo_interuption = True
        return

    def getMeasurementSettings(self ):
        settings =  (           
                     '\n#  ' + self.dl.measCond
                    +'\n#measurementDelay = '+ str(self.measurementDelay)
                    +'\n#measurementDuration = ' + str(self.measurementDuration )
        )
        return settings
    