import visa
import time
import numpy as np
import os


class SR7265():

    def __init__(self, address):
        rm = visa.ResourceManager()
        # print(rm.list_resources())
        self.ins = rm.open_resource(address)
        self.ins.timeout = 10000
        self.initialization_results = {}

    def SetupLockInSR7265(self):
        '''
        Get the Id of the lockin amplifier
        '''
        SCPI_Command = 'ID'
        self.initialization_results['result'] = self.ins.query(SCPI_Command)

        '''
        Get the version of the lockin amplifier
        '''
        SCPI_Command = 'VER'
        self.initialization_results['version'] = self.ins.query(SCPI_Command)

        '''
        Set the lockin amplifier in voltage mode
        '''
        SCPI_Command = 'IMODE 0'
        self.initialization_results['set current mode result'] = self.ins.write(
            SCPI_Command)

        '''
        Set single channel input
        '''
        SCPI_Command = 'VMODE 1'
        self.initialization_results['set voltage mode result'] = self.ins.write(
            SCPI_Command)

        '''
        Set coupling to DC
        '''
        SCPI_Command = 'CP 1'
        self.initialization_results['set coupling mode result'] = self.ins.write(
            SCPI_Command)

    def SetParameters(self, osc_amp, sensitivity, input_mode):
        ''' 
        Set the oscillator amplitude 
        '''
        SCPI_Command = 'OA. ' + str(osc_amp)
        b = self.ins.write(SCPI_Command)

        '''
        Set the sensitivity to: 
        '''
        SCPI_Command = 'SEN ' + str(sensitivity)
        b = self.ins.write(SCPI_Command)

        '''
        Set the gain to 50db , however this doesn't seem to work
        '''
        SCPI_Command = 'ACGAIN 5'
        b = self.ins.write(SCPI_Command)

        '''
        Voltage mode input device control
        '''
        SCPI_Command = 'FET ' + str(input_mode)
        b = self.ins.write(SCPI_Command)

    def measureMP(self, freq, correct_time_constant, time_to_wait_for_stable_signal):
        '''
        set frequency
        '''
        SCPI_Command = 'OF. ' + '%0.3f' % freq
        result = self.ins.write(SCPI_Command)

        '''
        set new time constant which is at least 5 times the time period 
        of given frequency
        '''
        SCPI_Command = 'TC ' + str(correct_time_constant)
        result = self.ins.write(SCPI_Command)

        measurement_count = 5
        if (time_to_wait_for_stable_signal < 1e-3):
            measurement_count = 3
        # measure the magnitude and phase of the signal
        # magnitude is given in volts (probably already multiplied by the AC gain)
        SCPI_Command = 'MP.'
        # let the measurement to be stable for 20 times the given time constant
        time.sleep(time_to_wait_for_stable_signal * 10)
        measurement = self.ins.query(SCPI_Command)
        measurement = measurement.replace('\x00', '')
        finalreal = float(measurement.split(',')[0])
        finalimag = float(measurement.split(',')[1])

        for i in range(measurement_count - 1):
            time.sleep(time_to_wait_for_stable_signal * 10 + 0.1)
            measurement = self.ins.query(SCPI_Command)
            measurement = measurement.replace('\x00', '')
            real = float(measurement.split(',')[0])
            imag = float(measurement.split(',')[1])
            finalreal = (real + finalreal)/2
            finalimag = (imag + finalimag)/2

        # compose back the measurement
        finalmeas = str(finalreal) + ',' + str(finalimag)

        return finalmeas

    def Turnoff(self):
        ''' 
        Set the oscillator amplitude  to zero
        '''
        SCPI_Command = 'OA. ' + str(0)
        b = self.ins.write(SCPI_Command)
