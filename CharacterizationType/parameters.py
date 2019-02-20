class GeneralParameters():
    def __init__(self, sampleName, deviceName, dataDir, measConditions,type_of_measurement):
        self.sampleName = sampleName
        self.deviceName = deviceName
        self.dataDir = dataDir
        self.measCond = measConditions
        self.type  = type_of_measurement

        
class Transferparameters():
    def __init__(self):

        self.Vds = 0.0
        self.doubleSweep = False
        #for single sweep
        self.Vgs_Start = 0.0
        self.Vgs_end  = 0.0
       
        # for double sweep
        self.startV  = 0.0
        self.Vgs_maxV  = 0.0
        self.Vgs_minV = 0.0
        self.Vgs_step  = 0.0
        self.sweepDelay=0.0
        self.number_of_transfer_meas = 0
        self.ins_k2636 = True
        self.ins_u2722a = False
        self.ig_limit_ms = 0.0
        self.id_limit_ms = 0.0

class Outputparameters():
    def __init__(self):
        
        self.Vgs = 0.0
        
        #for sweep 
        self.Vds_start = 0.0
        self.Vds_end = 0.0
        self.Vds_step = 0.0
        
        #for cyclic
        self.Vds_cyc_start = 0.0
        self.Vds_cyc_max = 0.0
        self.Vds_cyc_min = 0.0
        self.Vds_cyc_step = 0.0
        self.cycle_num = 0

        self.sweep_cyc = 0
        self.sweepDelay = 0.0
        self.ins_k2636 = True
        self.ins_u2722a = False
        self.ig_limit_ms = 0.0
        self.id_limit_ms = 0.0
        # self.osdelay=0.0

class ResistanceParameters():
    def __init__(self):
        
        self.Vds_Start = 0.0
        self.Vds_end = 0.0
        self.Vds_step = 0.0
        self.sweepDelay = 0.0
        self.ins_k2636 = True
        self.ins_u2722a = False

class Solparameters():
    def __init__(self):
        self.Vds = 0.0
        self.Vgs = 0.0
        self.Time = 0.0
        self.unlim_meas = False
        self.keep_vg = False
        self.keep_vd = False 
        self.type = r''
        self.solution = r''
        self.sweepDelay = 0.0
        self.ins_k2636 = True
        self.ins_u2722a = False
        self.vg_dc = True
        self.vg_ac = False

class ImpedanceParameters():
    def __init__(self):
        self.oscamp = 0.0
        self.startf = 0.0
        self.stopf = 0.0
        self.numofpoints = 0
        self.electrodes = r''
        self.solution = r''
        self.input_mode = 1
        

class ISEPotentiostatParameters():
    def __init__(self):
        self.datadir = r' '
        self.deviceNumber = r' '
        self.sampleNumber = r' '
        self.measurementInterval = 0 
        self.meastime = 1
        self.ChannelA = 1
        self.ChannelB = 1
        self.measurementConditions = r'forgot to input the measurement condition...  '

class  PotentiostatParameters():
    def __init__(self):
        self.measurementDelay = 0 
        self.measurementDuration = 0

class IGZOChannelProgParameters():
    def __init__(self):
        self.sampleNumber =  r' '
        self.measurementConditions =  r' '
        self.datadir =  r' '
        self.programmingChannel =  r' '
        self.CurrentLimit =  1e-5
        self.NumberOfPulses =  0
        self.pulseOn =  1e-3
        self.pulseOff =  1e-2


class twoterminalparameters():
    def __init__(self):
        self.sampleNumber =  r' '
        self.deviceNumber = r' '
        self.measurementConditions =  r' '
        self.datadir =  r' '
        self.commonvoltage = 0
        self.sweepDelay=0.0

class CyclicVoltammeteryParameters():
    def __init__(self):
        self.startV = 0.0
        self.endV = 0.0
        self.minV = 0.0
        self.step_size = 0
        self.scan_rate = 0.0
        self.cycles = 0 
        self.current_limit = 0.0