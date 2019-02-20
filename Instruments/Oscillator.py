import visa
import time

class K2636_Oscillator():
    
    def __init__(self):

        addr = 'GPIB0::27::INSTR'
        rm = visa.ResourceManager( )
        self.ins = rm.open_resource(addr)
        self.ins.write('reset()')
        self.ins.write('display.clear()')
        self.smu = 'smub'

    def ApplyVoltagePulse(self, pulseV, pulseOn):
        SCPI_Command =  self.smu + '.source.levelv = ' + str(pulseV)
        self.ins.write(SCPI_Command)
        time.sleep(pulseOn)
        SCPI_Command =  self.smu + '.source.levelv = ' + str(-1*pulseV)
        self.ins.write(SCPI_Command)
        time.sleep(pulseOn)

    def Configure(self):
        self.ins.write(self.smu + '.source.func = ' + self.smu + '.OUTPUT_DCVOLTS') 
        limiti = 1e-3
        self.ins.write(self.smu + '.source.limiti = {}'.format(limiti))
        self.ins.write(self.smu + '.measure.autorangei = ' + self.smu + '.AUTORANGE_ON')
        self.ins.write(self.smu +'.sense = ' +self.smu + '.SENSE_LOCAL')
        SCPI_Command = self.smu + '.source.output = ' + self.smu + '.OUTPUT_ON'
        self.ins.write(SCPI_Command)


    def TurnoffChannels(self):
        self.channeloff('smua')
        self.channeloff('smub')

def main():
    osc = K2636_Oscillator()
    osc.Configure()
    while True:
        osc.ApplyVoltagePulse(0.4, 1e-3)


if __name__ == '__main__':
    main()