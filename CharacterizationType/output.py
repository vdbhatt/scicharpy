import numpy as np
import pyqtgraph as pg
import threading
import time
from Instruments.Fake_K2636_GPIB import * 
from Utils.sweepUtils import *
from DataLogger.datalogger import datalogger
from DataProcessing.processData import processData
import arrow

class FuncThread(threading.Thread):
    def __init__(self,t,*a):
        self._t=t
        self._a=a
        threading.Thread.__init__(self)
    def run(self):
        self._t(*self._a)

class NANOBIO_OutputCharacterization():
    def __init__(self, measuringInstrument,op):
        ###---------------- MEASUREMENT PARAMETERS ----------------###
        self.deviceNumber = op.deviceNumber
        self.sampleNumber = op.sampleNumber
        self.measurementConditions = op.measurementConditions

        self.Vds_Start = op.Vds_Start
        self.Vds_end = op.Vds_end
        self.Vds_step = op.Vds_step
        
        self.Vgs_Start = op.Vgs_Start
        self.Vgs_end = op.Vgs_end
        self.Vgs_step = op.Vgs_step
        self.sweepDelay = op.sweepDelay
        self.datadir = op.datadir
        self.osdelay= op.osdelay

        self.measurementRange = 'auto'
        self.Sourcemode = 'DC_V'
        self.gate = 'smua'
        self.drain = 'smub'

        ##############################################################
        self.comment = self.getMeasurementSettings()        
        self.timestep = []
        self.Id = []
        self.Ig = []
        self.VdsBuffer = []
        self.VgsBuffer = []
        self.xdata = []
        self.idydata = []
        self.igydata = []
        self.timestamp = []
        
        self.measDate = arrow.now().format('YYYY-MM-DD')
        self.filename = 'output_' + self.measDate + r'S#'+self.sampleNumber + r'_D#' +self.deviceNumber
        self.dl = datalogger(self.datadir, self.filename, self.comment)
        self.filename = self.dl.filename

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
 
    def startMeasurement(self):
        dataAquistion_thread = FuncThread(self.executeDataAquisition)
        dataAquistion_thread.start()
        
        while self.measurementDone != True: 
            self.idcurve.setData(self.xdata, self.idydata)
            self.igcurve.setData(self.xdata, self.igydata)
            self.qapp.processEvents()

    def executeDataAquisition(self):
        self.measuringinstrument.Configure( self.measurementRange,  self.Sourcemode,  self.gate)
        self.measuringinstrument.Configure( self.measurementRange,  self.Sourcemode,  self.drain)
        self.measuringinstrument.channelon( self.gate)
        self.measuringinstrument.channelon( self.drain)
        self.measuringinstrument.measureId_VgsStep( self.gate,  self.drain, 0)
        
        Vgs = GetSweepVoltage( self.Vgs_Start,  self.Vgs_end,  self.Vgs_step)
        Vds = GetSweepVoltage( self.Vds_Start,  self.Vds_end,  self.Vds_step)
        measurementTime = 0
        for vgs_step in Vgs:
            self.measuringinstrument.setVoltage(self.gate, vgs_step)
            self.measuringinstrument.setVoltage(self.drain, 0)
            time.sleep(self.osdelay)
            
            for vds_step in Vds:
                t0 = time.time()
                measured_Id, measured_Ig = self.measuringinstrument.measureId_Ig_VdsStep(self.gate, self.drain,  vds_step)
                dt = time.time()-t0
                measurementTime += dt 
                time.sleep(self.sweepDelay)       
                self.Id.append(measured_Id)
                self.Ig.append(measured_Ig)
                self.VdsBuffer.append(vds_step)
                self.VgsBuffer.append(vgs_step)
                self.timestamp.append(measurementTime)                
                self.xdata = self.VdsBuffer
                self.idydata = self.Id
                self.igydata = self.Ig

        self.measuringinstrument.channeloff(self.gate)
        self.measuringinstrument.channeloff(self.drain)
        self.dl.saveOutput( self.Id, self.Ig, self.VdsBuffer, self.VgsBuffer, self.timestamp)
        time.sleep(1)
        self.measurementDone = True

    def getMeasurementSettings(self ):
        settings =  (
                     '\n#Vds_Start = '+ str(self.Vds_Start)
                    +'\n#Vds_end = ' + str(self.Vds_end )
                    +'\n#Vds_step  = ' + str(self.Vds_step )
                    +'\n#Vgs_Start  = ' + str(self.Vgs_Start )
                    +'\n#Vgs_end  = ' + str(self.Vgs_end )
                    +'\n#Vgs_step  = ' + str(self.Vgs_step)
                    +'\n#measurementRange = ' + str(self.measurementRange) 
                    +'\n#Sourcemode  = ' + str(self.Sourcemode )
                    +'\n#gate  = ' + str(self.gate )
                    +'\n#drain  = ' + str(self.drain) 
                    +'\n#sweepDelay  = ' + str(self.sweepDelay)
                    +'\n#  ' + self.measurementConditions
        )
        return settings