import visa
import time

class K2636_potentiostat():
    
    def __init__(self,address, selectedChannel):
        addr = str(address) + '::INSTR'
        rm = visa.ResourceManager( )
        self.ins = rm.open_resource(addr)
        self.ins.write('reset()')
        self.channel = selectedChannel


    def SetupPotentiostat(self):
        self.ins.write(self.channel  + '.source.func = ' + self.channel  + '.OUTPUT_DCAMPS')
        self.ins.write(self.channel  + '.source.limitv = 20')
        # self.ins.write('smua' +'.sense = ' + 'smua' + '.SENSE_REMOTE')
        self.ins.write(self.channel  + '.measure.autorangev = ' + self.channel  + '.AUTORANGE_ON')
        SCPI_Command = self.channel + '.source.output =' + self.channel +'.OUTPUT_ON'
        self.ins.write(SCPI_Command)

    def GetV_PotentiostatMode(self,measurementDelay):
        biasI = 0
        SCPI_Command =  self.channel + '.source.leveli = ' + str(biasI)
        self.ins.write(SCPI_Command)
        time.sleep(measurementDelay)
        SCPI_Command = 'print(' + self.channel + '.measure.v())'
        measured_V = float(self.ins.ask(SCPI_Command))
        return measured_V


    def channeloff(self,channel):
        SCPI_Command = channel + '.source.output =' + channel +'.OUTPUT_OFF'
        self.ins.write(SCPI_Command)

    def TurnoffChannels(self):
        self.channeloff('smua')
        self.channeloff('smub')