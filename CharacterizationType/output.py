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

class NANOBIO_OutputCharacterization():
    def __init__(self, measuringInstrument, op, datalogger):
        ###---------------- MEASUREMENT PARAMETERS ----------------###
        
        self.Vgs = op.Vgs 
        #for sweep
        self.Vds_start = op.Vds_start
        self.Vds_end = op.Vds_end
        self.Vds_step = op.Vds_step
        #for cyclic
        self.Vds_cyc_start = op.Vds_cyc_start
        self.Vds_cyc_max = op.Vds_cyc_max
        self.Vds_cyc_min = op.Vds_cyc_min
        self.Vds_cyc_step = op.Vds_cyc_step
        self.Cycle_num = op.cycle_num
        
        self.sweep_cyclic = op.sweep_cyc
        self.ig_limit_ms = op.ig_limit_ms
        self.id_limit_ms = op.id_limit_ms
        self.sweepDelay = op.sweepDelay
        self.measurementRange = 'auto'
        self.Sourcemode = 'DC_V'
        
        if op.ins_k2636:
            self.gate = 'smua'
            self.drain = 'smub'
        elif op.ins_u2722a:
            self.gate = 1
            self.drain = 2
        else:
            self.gate = 'smua'
            self.drain = 'smub'


        ##############################################################

        self.timestep = []
        self.Id = []
        self.Ig = []
        self.VdsBuffer = []
        self.xdata = []
        self.idydata = []
        self.igydata = []
        self.timestamp = []
        self.dl = datalogger
        
        ########## OBJECTS TO PLOT THE DATA #############
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
            self.dl.saveOutput(self.Id, self.Ig, self.VdsBuffer, self.VgsBuffer, self.timestamp)
            self.DataSaved = True
        self.measuringinstrument.channeloff(self.gate)
        self.measuringinstrument.channeloff(self.drain)
        self.measurementDone = True


    def executeDataAquisition(self):
        self.measuringinstrument.Configure( self.measurementRange,  self.Sourcemode,  self.gate, self.ig_limit_ms)
        self.measuringinstrument.Configure( self.measurementRange,  self.Sourcemode,  self.drain, self.id_limit_ms)
        set_range_counter = 5
        present_range_Ig = 10e-6
        present_range_Id = 10e-6
        self.measuringinstrument.channelon( self.gate)
        self.measuringinstrument.channelon( self.drain)
        self.measuringinstrument.setVoltage(self.gate, self.Vgs)
        self.measuringinstrument.measureId_VdsStep(self.drain, 0)

        self.dl.WriteMeasurementSettings(self.getMeasurementSettings())

        if self.sweep_cyclic == 0:   
            self.Vds = GetSweepVoltage(self.Vds_start, self.Vds_end, self.Vds_step)
        else :
            self.Vds = GetDoubleSweep(self.Vds_cyc_start, self.Vds_cyc_max, self.Vds_cyc_min, self.Vds_cyc_step, self.Cycle_num)
        rows_of_meas_data = np.zeros(len(self.Vds))
        self.Id = np.zeros(len(self.Vds))
        self.Ig = np.zeros(len(self.Vds))
        self.VgsBuffer = np.zeros(len(self.Vds))
        self.timestamp = np.zeros(len(self.Vds))
        self.VdsBuffer = np.zeros(len(self.Vds))
        
        measurementTime = 0

        for vds_index in range(len(self.Vds)):
            if self.clean_exit_signal:
                return
            t0 = time.time()
            measured_Id, measured_Ig = self.measuringinstrument.measureId_Ig_VdsStep(self.gate, self.drain, self.Vds[vds_index], self.sweepDelay)
            dt = time.time()-t0
            measurementTime += dt
            set_range_counter -=1
            ##########  FIX THE MEASUREMENT RANGE
            if set_range_counter <= 0:
                set_range_counter = 5
                present_range_Ig = self.measuringinstrument.SetRange(self.Sourcemode, measured_Ig, present_range_Ig, self.gate)
                present_range_Id = self.measuringinstrument.SetRange(self.Sourcemode, measured_Id, present_range_Id, self.drain)
            time.sleep(self.sweepDelay)
            
            self.Id[vds_index] = measured_Id
            self.Ig[vds_index] = measured_Ig
            self.VdsBuffer[vds_index] = self.Vds[vds_index]
            self.VgsBuffer[vds_index] = self.Vgs
            self.timestamp[vds_index] = measurementTime
            self.xdata.append(self.Vds[vds_index])
            self.idydata.append(measured_Id)
            self.igydata.append(measured_Ig)
        self.measurementDone = True
        self.measurement_finished_wo_interuption = True
        return

    def getMeasurementSettings(self ):
        if self.sweep_cyclic == 0 :
            settings =  (
                        '\n# ' + self.dl.measCond
                        +'\n# Vgs = '+ str(self.Vgs)
                        +'\n# Vds_start = '+ str(self.Vds_start)
                        +'\n# Vds_end = '+ str(self.Vds_end)
                        +'\n# Vds_step = '+ str(self.Vds_step)
                        +'\n# measurementRange = ' + str(self.measurementRange) 
                        +'\n# Sourcemode  = ' + str(self.Sourcemode )
                        +'\n# gate  = ' + str(self.gate )
                        +'\n# drain  = ' + str(self.drain) 
                        +'\n# sweepDelay  = ' + str(self.sweepDelay)
            )
        else : 
            settings =  (
                        '\n# ' + self.dl.measCond
                        +'\n# Vgs = '+ str(self.Vgs)
                        +'\n# Vds_start = '+ str(self.Vds_cyc_start)
                        +'\n# Vds_max = ' + str(self.Vds_cyc_max )
                        +'\n# Vds_min = ' + str(self.Vds_cyc_min )
                        +'\n# Vds_step  = ' + str(self.Vds_cyc_step )
                        +'\n# cycles = ' + str(self.Cycle_num)
                        +'\n# measurementRange = ' + str(self.measurementRange) 
                        +'\n# Sourcemode  = ' + str(self.Sourcemode )
                        +'\n# gate  = ' + str(self.gate )
                        +'\n# drain  = ' + str(self.drain) 
                        +'\n# sweepDelay  = ' + str(self.sweepDelay)
            )
        return settings