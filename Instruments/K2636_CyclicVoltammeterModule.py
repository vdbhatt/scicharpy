import visa
import time

class K2636_CyclicVoltammeter():
    
    def __init__(self,address):
        addr = str(address) + '::INSTR'
        rm = visa.ResourceManager( )
        self.ins = rm.open_resource(addr)
        self.ins.write('reset()')

    def measureI_VStep(self, channel, v_step, step_delay):
        SCPI_Command =  channel + '.source.levelv = ' + str(v_step)
        self.ins.write(SCPI_Command)
        time.sleep(step_delay)
        SCPI_Command = 'print(' + channel + '.measure.i())'
        measured_I = float(self.ins.ask(SCPI_Command))
        return measured_I  

    def SetRange(self, Sourcemode, present_current_value, present_range, smu):
        selected_range = 10e-3
        avail_ranges = (100e-9, 1e-6, 10e-6, 100e-6, 1e-3, 10e-3)
        for current_range in avail_ranges:
            if present_current_value < current_range:
                selected_range = current_range
                break
        if present_range == selected_range:
            return selected_range

        if Sourcemode == 'DC_V':
            self.ins.write(smu + '.source.measure.autorangei = ' + smu + '.AUTORANGE_OFF')
            self.ins.write(smu + '.rangei = ' + str(selected_range) )
        
        return selected_range


    def SetupVoltammeter(self, measurementRange, Sourcemode, smu, current_limit):
        if Sourcemode == 'DC_V':
            self.ins.write(smu + '.source.func = ' + smu + '.OUTPUT_DCVOLTS')
            if measurementRange=='auto':
                limiti = current_limit
                self.ins.write(smu + '.source.limiti = {}'.format(limiti))
                self.ins.write(smu + '.source.measure.autorangei = ' + smu + '.AUTORANGE_OFF')
                self.ins.write(smu + '.rangei = ' + str(1e-7) )
                self.ins.write(smu +'.sense = ' + smu + '.SENSE_REMOTE')
                self.ins.write(smu + '.source.output = ' + smu + '.OUTPUT_ON')
            else:
                self.ins.write(smu + '.source.limiti = {}'.format(limiti))
                self.ins.write(smu + '.measure.rangei = {}'.format(measurementRange))

    def channeloff(self, channel):
        SCPI_Command = channel + '.source.output =' + channel +'.OUTPUT_OFF'
        self.ins.write(SCPI_Command)

    def TurnoffChannels(self):
        self.channeloff('smua')
        self.channeloff('smub')