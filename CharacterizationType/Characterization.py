

from Instruments.Fake_K2636_GPIB import * 
from Instruments.K2636_GPIB import * 
from DataLogger.datalogger import datalogger
from CharacterizationType.OnlineMeas import NANOBIO_OnlineMeas
from CharacterizationType.parameters import *
from DataProcessing.processData import processData
from CharacterizationType.transfer import *
from CharacterizationType.channelResistance import *

class TransistorCharacterizationTasks():

    def __init__(self):
        self.online_meas_instrument = Fake_K2636_GPIB(r'GPIB0::27')
        self.transfer_meas_instrument = Fake_K2636_GPIB(r'GPIB0::16')
        self.resistance_meas_instrument = Fake_K2636_GPIB(r'GPIB0::27')
        self.resistance_characterizer = None
        self.online_characterizer  = None
        self.transfer_characterizer  = None
        
    
    def runOnline(self, sample, device,comments, datadir, ui_vg, ui_vd, ui_timebsa, ui_timeprotein, ui_namebsa, ui_nameprotein, id_limit, ig_limit, ui_sweepdelay, protein_bsa):
        
        gp = GeneralParameters(sample,device,datadir,comments,"online")
        sp = Solparameters()
        sp.Vds= ui_vd
        sp.Vgs= ui_vg
        sp.sweep_delay_ms = ui_sweepdelay * 1e-03  
        sp.id_limit_ms = id_limit *1e-03
        sp.ig_limit_ms = ig_limit *1e-03

        if protein_bsa == 0:
            sp.Time = ui_timebsa.minute()*60 + ui_timebsa.second()
            sp.type = 'BSA'
            sp.solution = ui_namebsa
        else : 
            sp.Time = ui_timeprotein.minute()*60 + ui_timeprotein.second()
            sp.type = 'Protein'
            sp.solution = ui_nameprotein
        try:
            dl = datalogger(gp)
            
            self.online_characterizer = NANOBIO_OnlineMeas(self.online_meas_instrument,sp,dl) 
            self.online_characterizer.startMeasurement()
            print("processing Image")
            self.data_processor = processData(dl.filePath)
            self.data_processor.saveOnlineCharacteristics()
            print('All done ! ')
        except:
            print("aborting ! ")
        
        self.online_meas_instrument.TurnoffChannels()
    
    def StopOnline(self):
        self.online_characterizer.measurementDone = True

    def RunTransfer(self, sample, device, comments, datadir, ui_Vgstart, ui_Vgmax, ui_Vgmin, ui_Vgstep, ui_cycles, ui_Vd, id_limit, ig_limit, ui_sweepdelay):
        gp = GeneralParameters(sample, device, datadir, comments, "transfer")

        ### transfer characterization parameters
        tp = Transferparameters()
        tp.Vds = ui_Vd
        tp.doubleSweep = True
        #for single sweep
        tp.Vgs_Start = 0.8
        tp.Vgs_end = -0.8

        # for double sweep
        tp.startV = ui_Vgstart
        tp.Vgs_maxV = ui_Vgmax
        tp.Vgs_minV = ui_Vgmin
        tp.Vgs_step = ui_Vgstep
        tp.sweepDelay = ui_sweepdelay * 1e-03
        tp.number_of_transfer_meas = ui_cycles
        tp.id_limit_ms = id_limit *1e-03 
        tp.ig_limit_ms = ig_limit *1e-03
        
        ###
        try:
            dl = datalogger(gp)
            # for transfers in range():
            self.transfer_characterizer = NANOBIO_TransferCharacterization(self.transfer_meas_instrument,tp,dl) 
            self.transfer_characterizer.startMeasurement()
            print("processing Image")
            self.data_processor = processData(dl.filePath)
            self.data_processor.saveTransferCharacteristics()
            print('transfer characterization done ! ')
        except:
            print('something happened')
        self.transfer_meas_instrument.TurnoffChannels()

    def StopTransfer(self):
        self.transfer_characterizer.measurementDone = True


    def runResistance (self, sample, device, comments, datadir, ui_vdstart, ui_vdmax, ui_vdmin, ui_vdstep, ui_cycles, id_limit, ui_sweepdelay):
        gp = GeneralParameters(sample, device, datadir, comments, 'resistance')

        ################# Channel Resistance  #################
        rp = ResistanceParameters()
        rp.Vds_Start = ui_vdstart
        rp.Vds_max = ui_vdmax
        rp.Vds_min = ui_vdmin
        rp.Vds_step = ui_vdstep
        rp.sweepDelay = ui_sweepdelay * 1e-03
        rp.number_of_res_meas = ui_cycles
        rp.id_limit_ms = id_limit *1e-03

        
        try:
            dl = datalogger(gp)
            #for res in range(number_of_res_meas):
            self.resistance_characterizer =  NANOBIO_ChannelResistance(self.resistance_meas_instrument,rp,dl)
            self.resistance_characterizer.startMeasurement()
            print("processing image")
            self.data_processor = processData(dl.filePath)
            self.data_processor.saveResistanceCharacteristics()
            print("resistance characterization done !")
        except:
            print('something happened')
        self.resistance_meas_instrument.TurnoffChannels()

    def StopResistance(self):
        self.resistance_characterizer.measurementDone = True

    