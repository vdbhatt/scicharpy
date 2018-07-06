import visa
import numpy as np
import time 


class Fake_K2636_GPIB():
    
    def __init__(self,address):
        addr = str(address) + '::INSTR'
        # rm = visa.ResourceManager( )
        # self.ins = rm.open_resource(addr)
        # #self.ins.write('reset()')

    def measureId_VgsStep(self, gate, drain, vgs_step):
        return vgs_step

    def measureId_Ig_VgsStep(self, gate, drain, vgs_step, wait_before_measure):
        vth = 0.032
        time.sleep(wait_before_measure)
        Id = 1.5e-4* np.random.rand()
        Ig = 1.5e-6*np.random.rand()
        return Id, Ig


    def measureId_VdsStep(self,  drain, vds_step):

        return vds_step

    def measureId_Ig_VdsStep(self,  gate, drain, vds_step):
        SCPI_Command =  drain + '.source.levelv = ' + str(vds_step)
        #self.ins.write(SCPI_Command)
        SCPI_Command = 'print(' + drain + '.measure.i())'
        # measured_Id = float(self.ins.ask(SCPI_Command))
        SCPI_Command = 'print(' + gate + '.measure.i())'
        # measured_Ig = float(self.ins.ask(SCPI_Command))
        #return measured_Id,  measured_Ig
        return 36, 45 

    def measureI(self,voltage,commonvoltage):
        SCPI_Command =  voltage + '.source.levelv = ' + str(commonvoltage)
        #self.ins.write(SCPI_Command)
        SCPI_Command = 'print(' + voltage + '.measure.i())'
        # measured_Id = float(self.ins.ask(SCPI_Command))
        #return measured_Id 
        return 55


    def ApplyVoltagePulse(self, pulseV, pulseOn):
        SCPI_Command =  smu + '.source.levelv = ' + str(pulseV)
        #self.ins.write(SCPI_Command)
        time.sleep(pulseOn)
        SCPI_Command =  smu + '.source.levelv = ' + str(0)
        #self.ins.write(SCPI_Command)

    def GetV_PotentiostatMode(self,smu):
        biasI = 0
        SCPI_Command =  smu + '.source.leveli = ' + str(biasI)
        #self.ins.write(SCPI_Command)
        SCPI_Command = 'print(' + smu + '.measure.v())'
        # measured_V = float(self.ins.ask(SCPI_Command))
        #return measured_V
        return 3

    def GetVoutinv(self,Vin,Vout,Vstep):
        SCPI_Command =  Vin + '.source.levelv = ' + str(Vstep)
        #self.ins.write(SCPI_Command)
        SCPI_Command = 'print(' + Vout + '.measure.v())'
        measured_Vout = float(self.ins.ask(SCPI_Command))
        #return measured_Vout
        return 

    def Config_PotentiostatMode(self,Vout):
        #self.ins.write(Vout + '.source.func = ' + Vout + '.OUTPUT_DCAMPS')
        #self.ins.write(Vout + '.source.limitv = 20')
        #self.ins.write(Vout + '.measure.autorangev = ' + Vout + '.AUTORANGE_ON')
        pass



    def Configure(self, measurementRange, Sourcemode, smu, current_limit):
        pass
                
    def ConfigureIGZOChannelProgramming(self, CurrentLimit, Sourcemode, smu):
        pass

    def SetRange(self, present_current_value, present_range, smu):
        selected_range = 10e-3
        avail_ranges = (100e-9, 1e-6, 10e-6, 100e-6, 1e-3, 10e-3)
        for current_range in avail_ranges:
            if present_current_value < current_range:
                selected_range = current_range
                print("range changed from %s to %s" %(present_range, selected_range))

                break
        if present_range == selected_range:
            return selected_range

        # if Sourcemode == 'DC_V':
        #     pass
            # self.ins.write(smu + '.source.measure.autorangei = ' + smu + '.AUTORANGE_OFF')
            # self.ins.write(smu +'.rangei' = selected_range )
        
        return selected_range

           


    def ConfigurePotentiostat(self, channelA, channelB):
        pass
        #self.ins.write(channelA + '.source.func = ' + channelA + '.OUTPUT_DCAMPS')
        #self.ins.write(channelA + '.source.limitv = 20')
        #self.ins.write(channelA + '.measure.autorangev = ' + channelA + '.AUTORANGE_ON')
        #self.ins.write(channelB + '.source.func = ' + channelB + '.OUTPUT_DCAMPS')
        #self.ins.write(channelB + '.source.limitv = 20')
        #self.ins.write(channelB + '.measure.autorangev = ' + channelB + '.AUTORANGE_ON')

    def GetResistance(self,smu):
        SCPI_Command = 'print(' + smu + '.measure.r())'
        measured_R = float(self.ins.ask(SCPI_Command))
        return measured_R
        #return 3000


    def channelon(self, channel):
        SCPI_Command = channel + '.source.output = ' + channel + '.OUTPUT_ON'
        #self.ins.write(SCPI_Command)

    def channeloff(self, channel):
        SCPI_Command = channel + '.source.output =' + channel +'.OUTPUT_OFF'
        #self.ins.write(SCPI_Command)

    def setVoltage(self,channel,voltage):
        SCPI_Command =  channel + '.source.levelv = ' + str(voltage)
        #self.ins.write(SCPI_Command)

    def TurnoffChannels(self):
        self.channeloff('smua')
        self.channeloff('smub')