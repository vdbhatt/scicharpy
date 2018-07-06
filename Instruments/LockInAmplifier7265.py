import visa
import time
from LookUpTable import GetTimeConstantLUT
from SensitivityTable import GetSensitivity
import numpy as np
import os

class SR7265():
    
    def __init__(self):
        rm = visa.ResourceManager( )
        print(rm.list_resources())
        self.ins = rm.open_resource('GPIB0::12::INSTR')
        self.ins.timeout = 5000
        self.initialization_results = {}

    def SetupLockInSR7265(self):
        '''
        Get the Id of the lockin amplifier
        '''
        SCPI_Command =  'ID'
        self.initialization_results['result'] = l.ins.query(SCPI_Command)

        '''
        Get the version of the lockin amplifier
        '''
        SCPI_Command =  'VER'
        self.initialization_results['version'] = l.ins.query(SCPI_Command)

        '''
        Set the lockin amplifier in voltage mode
        '''
        SCPI_Command = 'IMODE 0'
        self.initialization_results['set current mode result'] = l.ins.write(SCPI_Command)

        '''
        Set single channel input
        '''
        SCPI_Command = 'VMODE 1'
        self.initialization_results['set voltage mode result'] = l.ins.write(SCPI_Command)

        '''
        Set coupling to DC
        '''
        SCPI_Command = 'CP 1'
        self.initialization_results['set coupling mode result'] = l.ins.write(SCPI_Command)


l = SR7265()
l.SetupLockInSR7265()
time_const_lookup = GetTimeConstantLUT()
instrument = l.ins
''' 
Set the oscillator amplitude 
'''
osc_amp = 0.2

#default parameters in case you don't get the result from Sensitivity table. However it should work
correct_sensitivity = 27
cntr = 0
amplitude = osc_amp
sensitivityLUT = GetSensitivity()

for sensitivity in sensitivityLUT : 
    if amplitude <= sensitivity:
        correct_sensitivity = cntr
        break
    cntr += 1

SCPI_Command = 'OA. '+ str(osc_amp)
print(SCPI_Command)
b = instrument.write(SCPI_Command)

'''
Set the sensitivity to: 
'''

SCPI_Command = 'SEN '+ str(correct_sensitivity)
print(SCPI_Command)
b = instrument.write(SCPI_Command)
'''
Set the gain to 50db , however this doesn't seem to work
'''
SCPI_Command = 'ACGAIN 5'   
b = instrument.write(SCPI_Command)

# set parameters for frequency sweep
start_f = 100 # in hertz 
stop_f = 250000 # in hertz



#generate the frequency in log scale. 
freq_array  = np.logspace(np.log10(start_f), np.log10(stop_f), num=250)
#default parametes in case no match are found ( however there should always be a match)
correct_time_constant = 29
time_to_wait_for_stable_signal = 100e3

#open a new file in append mode to save the data
folder = r'C:\Users\lockinanalysis'
fileName = 'S9_impedance_3-4.csv'
datafile = open(os.path.join(folder,fileName), "a")

for freq in freq_array:
    counter = 0
    time_period = 5.0/freq
    for timeconstant in time_const_lookup:
        if time_period <= timeconstant :
            correct_time_constant = counter
            time_to_wait_for_stable_signal = time_period
            break
        counter += 1
    # set new frequency upto 3 places after decimal
    SCPI_Command = 'OF. ' + '%0.3f' %freq
    result = instrument.write(SCPI_Command)
    # set new time constant which is atleast 5 times the time period 
    # of given frequency
    SCPI_Command = 'TC '+ str(correct_time_constant)
    result = instrument.write(SCPI_Command)

    # let the measurement to be stable for 10 times the given time constant
    time.sleep(time_to_wait_for_stable_signal * 20 )

    # measure the magnitude and phase of the signal 
    # magnitude is given in volts (probably already multiplied by the AC gain)
    SCPI_Command = 'MP.'
    measurement = instrument.query(SCPI_Command)

    print(freq)
    print(measurement)  
    #save the file in simple csv format
    dataline = str(freq) + ', '+ str(measurement).strip('\x00')
    datafile.write(dataline)
    #wait for the file to be written 
    time.sleep(1)

#close file after all the measurements are done
datafile.close()