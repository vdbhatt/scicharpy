import visa
import time

class U2722A_USB():
       
    def __init__(self, address=None):
        addr = 'USB0::0x0957::0x4118::MY56310003::INSTR'
        rm = visa.ResourceManager()
        self.ins = rm.open_resource(addr)
        
    def queryConnection(self):
       print(self.ins.query('SYST:CHAN?'))
        

    def measureId_VgsStep(self, gate, drain, vgs_step):
        gate = str(gate)
        drain = str(drain)
        SCPI_Command =  'VOLT '+ str(vgs_step) + ', (@' + gate + ')'
        self.ins.write(SCPI_Command)
        SCPI_Command = 'MEAS:CURR? '+ '(@' + drain + ')'
        measured_Id = float(self.ins.query(SCPI_Command))
        return measured_Id  

    def setVoltage(self,channel,voltage):
        
        SCPI_Command =  'VOLT:LIM 20, (@2)'
        self.ins.write(SCPI_Command)
        SCPI_Command =  'VOLT:RANG R20V, (@2)'
        self.ins.write(SCPI_Command)

        SCPI_Command =  'VOLT '+ str(voltage) + ', (@' + str(channel) + ')'
        self.ins.write(SCPI_Command)


    def measureId_Ig_VgsStep(self, gate, drain, vgs_step,wait_before_measure):
        gate = str(gate)
        drain = str(drain)
        SCPI_Command =  'VOLT '+ str(vgs_step) + ', (@' + gate + ')'
        self.ins.write(SCPI_Command)
        time.sleep(wait_before_measure)
        SCPI_Command = 'MEAS:CURR? '+ '(@' + drain + ')'
        measured_Id = float(self.ins.query(SCPI_Command))
        SCPI_Command = 'MEAS:CURR? '+ '(@' + gate + ')'
        measured_Ig = float(self.ins.query(SCPI_Command))
        return measured_Id, measured_Ig


    def measureId_VdsStep(self,  drain, vds_step):
        drain = str(drain)
        SCPI_Command =  'VOLT '+ str(vds_step) + ', (@' + drain + ')'
        self.ins.write(SCPI_Command)
        SCPI_Command = 'MEAS:CURR? '+ '(@' + drain + ')'
        measured_Id = float(self.ins.query(SCPI_Command))
        return measured_Id

    def measureId_Ig_VdsStep(self,  gate, drain, vds_step):
        gate = str(gate)
        drain = str(drain)
        SCPI_Command =  'VOLT '+ str(vds_step) + ', (@' + drain + ')'
        self.ins.write(SCPI_Command)
        SCPI_Command = 'MEAS:CURR? '+ '(@' + drain + ')'
        measured_Id = float(self.ins.query(SCPI_Command))
        SCPI_Command = 'MEAS:CURR? '+ '(@' + gate + ')'
        measured_Ig = float(self.ins.query(SCPI_Command))
        return measured_Id,  measured_Ig 

    def SetRange(self, Sourcemode, present_current_value, present_range, smu):
        present_current_value = abs(present_current_value)
        print(present_current_value)
        selected_range = 10e-3
        avail_ranges = (1e-6, 10e-6, 100e-6, 1e-3, 10e-3)
        for current_range in avail_ranges:
            if present_current_value < current_range:
                selected_range = current_range
                break
        if present_range == selected_range:
            print('selected range is ' + str(selected_range))
            return selected_range
        
        if selected_range == 1e-6 :
            range_to_set = 'R1uA'
        elif selected_range == 10e-6 :
            range_to_set = 'R10uA'
        elif selected_range == 100e-6 :
            range_to_set = 'R100uA'
        elif selected_range ==  1e-3:
            range_to_set = 'R1mA'    
        elif selected_range ==  10e-3:
            range_to_set = 'R10mA'  

        command = 'CURR:RANG ' + range_to_set +  ' , (@' + str(smu) + ')'
        print('updating the range  :  ')
        print(command)
        self.ins.write(command)
        return selected_range


    def Configure(self, measurementRange=None, Sourcemode=None, smu=None, current_limit=None):
        #self.ins.write('CURR:LIM 0.12, (@' + str(1) + ')')
        self.ins.write('CURR:RANG R10uA, (@' + str(1) + ')')
        #self.ins.write('CURR:LIM 0.12, (@' + str(2) + ')')
        self.ins.write('CURR:RANG R10uA, (@' + str(2) + ')')
        
        SCPI_Command =  'VOLT:LIM 20, (@2)'
        self.ins.write(SCPI_Command)
        SCPI_Command =  'VOLT:RANG R20V, (@2)'
        self.ins.write(SCPI_Command)
        
        # command = 'VOLT 0, (@1)'
        # command = 'VOLT 0, (@2)'
        # command = 'VOLT 0, (@3)'
        self.channelon(1)
        self.channelon(2)

    def channelon(self, channel):
        SCPI_Command = 'output ON, (@' + str(channel) + ')'
        self.ins.write(SCPI_Command)

    def channeloff(self, channel):
        SCPI_Command = 'output OFF, (@' + str(channel) + ')'
        self.ins.write(SCPI_Command)

    def TurnoffChannels(self):
        self.channeloff(1)
        self.channeloff(2)
        self.channeloff(3)