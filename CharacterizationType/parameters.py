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

class Outputparameters():
    def __init__(self):
        self.deviceNumber = r' '
        self.sampleNumber = r' '
        self.datadir = r' '
        self.measurementConditions = r' '

        self.Vds_Start = 0.0
        self.Vds_end = 0.0
        self.Vds_step = 0.0
        
        self.Vgs_Start = 0.0
        self.Vgs_end = 0.0
        self.Vgs_step = 0.0
        self.sweepDelay = 0.0
        self.osdelay=0.0

class ResistanceParameters():
    def __init__(self):
        
        self.Vds_Start = 0.0
        self.Vds_end = 0.0
        self.Vds_step = 0.0
        self.sweepDelay = 0.0

class Solparameters():
    def __init__(self):
        self.Vds = 0.0
        self.Vgs = 0.0
        self.Time=0.0
        self.type = r''
        self.solution = r''
        self.sweepDelay = 0.0
        

class ISEPotentiostatParameters():
    def __init__(self):
        self.datadir = r' '
        self.deviceNumber = r' '
        self.sampleNumber = r' '
        self.measurementInterval =0 
        self.meastime = 1
        self.ChannelA = 1
        self.ChannelB = 1
        self.measurementConditions = r'forgot to input the measurement condition...  '
        

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