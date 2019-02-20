import numpy as np
import pyqtgraph as pg
import threading
import time
from Utils.converter import *


from DataLogger.datalogger import datalogger
from DataProcessing.processData import processData
import arrow
from Utils.FuncThread import FuncThread
import Instruments.SR7265_SensitivityTable 
import Instruments.SR7265_TC_LUT

class NANOBIO_impedance():
    def __init__(self, measuringInstrument, ip, datalogger):
       
        ###---------------- MEASUREMENT PARAMETERS ----------------### 
        self.oscamp = ip.oscamp
        self.startf = ip.startf
        self.stopf = ip.stopf
        self.numofpoints = ip.numofpoints
        self.electrodes = ip.electrodes
        self.solution = ip.solution
        self.input_mode = ip.input_mode

        ##############################################################
        self.timestep = []
        self.Zimag = []
        self.Zreal = []
        self.frequency = []
        self.rawmeasurement = []
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
            self.dl.saveImpedance(self.frequency, self.Zreal, self.Zimag, self.rawmeasurement, self.timestamp)
            self.DataSaved = True
        self.measurementDone = True
        self.measuringinstrument.Turnoff()

    def executeDataAquisition(self):
        self.measuringinstrument.SetupLockInSR7265()
        # set_range_counter = 5
        # present_range_Id = 1e-03
        self.dl.WriteMeasurementSettings(self.getMeasurementSettings())
        
        # Vds = GetDoubleSweep (self.Vds_Start, self.Vds_max, self.Vds_min, self.Vds_step, self.number_of_res_meas)
        
        measurementTime = 0
        time_const_lookup = Instruments.SR7265_TC_LUT.GetTimeConstantLUT()
        sensitivityLUT = Instruments.SR7265_SensitivityTable.GetSensitivity()
        self.correct_sensitivity = 27
        cntr = 0
        amplitude = self.oscamp
        
        for sensitivity in sensitivityLUT : 
            if amplitude <= sensitivity:
                self.correct_sensitivity = cntr
                break
            cntr += 1

        self.measuringinstrument.SetParameters(self.oscamp, self.correct_sensitivity, self.input_mode)

        # set parameters for frequency sweep
        # start_f = 100 # in hertz 
        # stop_f = 250000 # in hertz
        #generate the frequency in log scale. 
        freq_array  = np.logspace(np.log10(self.startf), np.log10(self.stopf), num=self.numofpoints)

        #default parametes in case no match are found ( however there should always be a match)
        correct_time_constant = 29
        time_to_wait_for_stable_signal = 100e3
        for freq in freq_array:
            if self.clean_exit_signal:
                return
            counter = 0
            time_period = 5.0/freq
            for timeconstant in time_const_lookup:
                if time_period <= timeconstant :
                    self.correct_time_constant = counter
                    self.time_to_wait_for_stable_signal = time_period
                    break
                counter += 1
            t0 = time.time()
            measurement = self.measuringinstrument.measureMP(freq, self.correct_time_constant, self.time_to_wait_for_stable_signal)
            dt = time.time()-t0
            measurement = measurement.replace('\x00', '')
            real, imag = poltocart(float(measurement.split(',')[0]), float(measurement.split(',')[1]))
            measurementTime += dt 

            vin = self.oscamp
            vout =  np.empty([1,], dtype=complex)
            vout.real = real
            vout.imag = imag
            Z = 1000*vout[0]/(vin -vout[0])

            self.Zreal.append(Z.real)
            self.Zimag.append(-1*Z.imag)
            self.frequency.append(freq)
            self.rawmeasurement.append(measurement)
            self.timestamp.append(measurementTime)                
            self.xdata = self.Zreal
            self.ydata = self.Zimag

        self.measurementDone = True
        self.measurement_finished_wo_interuption = True
        return

    def getMeasurementSettings(self ):
        settings =  (           
                     '\n#  ' + self.dl.measCond
                    +'\n#Osc amp = '+ str(self.oscamp) + r' V'
                    +'\n#Start f = ' + str(self.startf ) + r' Hz'
                    +'\n#Stop f = ' + str(self.stopf )+ r' Hz'
                    +'\n#Points  = ' + str(self.numofpoints )
                    +'\n#Solution = ' + str(self.solution) 
                    +'\n#Electrodes  = ' + str(self.electrodes )
        )
        return settings
    