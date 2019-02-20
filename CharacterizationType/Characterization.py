from Instruments.Fake_K2636_GPIB import * 
from Instruments.K2636_GPIB import *
from Instruments.K2636_CyclicVoltammeterModule import * 
from Instruments.LockInAmplifier7265 import * 
from Instruments.K2636_PotentiostatModule import *
from Instruments.U2722A import *
from DataLogger.datalogger import datalogger
from CharacterizationType.OnlineMeas import NANOBIO_OnlineMeas
from CharacterizationType.parameters import *
from CharacterizationType.impedance import *
from CharacterizationType.cyclicvoltammeter import *
from CharacterizationType.potentiostatmodule import *
from DataProcessing.processData import processData
from CharacterizationType.transfer import *
from CharacterizationType.output import *
from CharacterizationType.channelResistance import *
from Utils.Communications import send_email

class TransistorCharacterizationTasks():

    def __init__(self):
        self.online_meas_instrument = None
        self.transfer_meas_instrument = None 
        self.resistance_meas_instrument = None 
        self.impedance_meas_instrument = None 
        self.cyclic_voltammeter_instrument = None 
        self.potentiostatInstrument = None
        self.resistance_characterizer = None
        self.online_characterizer  = None
        self.transfer_characterizer  = None
        self.impedance_characterizer = None
        self.cv_characterizer = None
        self.output_characterizer = None


    def runOnline(self, sample, device,comments, datadir, ui_K2636, ui_U2722A, ui_vg_DC, ui_vg_AC, ui_vg, ui_vd, ui_timebsa, ui_timeprotein, ui_timeion, ui_check_BSA, ui_check_protein, ui_check_ion, ui_namebsa, ui_nameprotein, ui_nameion, id_limit, ig_limit, ui_sweepdelay, protein_bsa, ui_keep_vg, ui_keep_vd):
        
        if ui_K2636:
            self.online_meas_instrument = K2636_GPIB(r'GPIB0::27')
        elif ui_U2722A:
            self.online_meas_instrument = U2722A_USB()
        else:
            self.online_meas_instrument = K2636_GPIB(r'GPIB0::27')

        gp = GeneralParameters(sample,device,datadir,comments,"online")
        sp = Solparameters()
        sp.Vds= ui_vd
        sp.Vgs= ui_vg
        sp.sweep_delay_ms = ui_sweepdelay * 1e-03  
        sp.id_limit_ms = id_limit *1e-03
        sp.ig_limit_ms = ig_limit *1e-03
        sp.keep_vg = ui_keep_vg
        sp.keep_vd = ui_keep_vd
        sp.ins_k2636 = ui_K2636
        sp.ins_u2722a = ui_U2722A
        sp.vg_dc = ui_vg_DC
        sp.vg_ac = ui_vg_AC
    
        if protein_bsa == 0:
            sp.Time = ui_timebsa.minute()*60 + ui_timebsa.second()
            sp.unlim_meas = ui_check_BSA
            sp.type = 'BSA'
            sp.solution = ui_namebsa
        elif protein_bsa == 1: 
            sp.Time = ui_timeprotein.minute()*60 + ui_timeprotein.second()
            sp.unlim_meas = ui_check_protein
            sp.type = 'Protein'
            sp.solution = ui_nameprotein
        else :
            sp.Time = ui_timeion.minute()*60 + ui_timeion.second()
            sp.unlim_meas = ui_check_ion
            sp.type = 'Ions'
            sp.solution = ui_nameion
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

    def PauseOnline(self):
        self.online_characterizer.measurementPause = True

    def ContinueOnline(self):
        self.online_characterizer.measurementContinue = True

    def UpdateOnline(self, sample, device, comments, datadir, ui_K2636, ui_U2722A, ui_vg_DC, ui_vg_AC, ui_vg, ui_vd, ui_timebsa, ui_timeprotein, ui_timeion, ui_check_BSA, ui_check_protein, ui_check_ion, ui_namebsa, ui_nameprotein, ui_nameion, id_limit, ig_limit, ui_sweepdelay, protein_bsa, ui_keep_vg, ui_keep_vd):

        gp = GeneralParameters(sample,device,datadir,comments,"online")
        sp = Solparameters()
        sp.Vds= ui_vd
        sp.Vgs= ui_vg
        sp.sweep_delay_ms = ui_sweepdelay * 1e-03  
        sp.id_limit_ms = id_limit *1e-03
        sp.ig_limit_ms = ig_limit *1e-03
        sp.keep_vg = ui_keep_vg
        sp.keep_vd = ui_keep_vd
        sp.ins_k2636 = ui_K2636
        sp.ins_u2722a = ui_U2722A
        sp.vg_dc = ui_vg_DC
        sp.vg_ac = ui_vg_AC

        if protein_bsa == 0:
            sp.Time = ui_timebsa.minute()*60 + ui_timebsa.second()
            sp.unlim_meas = ui_check_BSA
            sp.type = 'BSA'
            sp.solution = ui_namebsa
        elif protein_bsa == 1: 
            sp.Time = ui_timeprotein.minute()*60 + ui_timeprotein.second()
            sp.unlim_meas = ui_check_protein
            sp.type = 'Protein'
            sp.solution = ui_nameprotein
        else :
            sp.Time = ui_timeion.minute()*60 + ui_timeion.second()
            sp.unlim_meas = ui_check_ion
            sp.type = 'Ions'
            sp.solution = ui_nameion
        try:
            self.online_characterizer.updateMeasValues = True
            self.online_characterizer.updateValues(sp)
            print("processing Image")
        except:
            print("unable to update online values")

    def RunTransfer(self, sample, device, comments, datadir, ui_K2636, ui_U2722A, ui_Vgstart, ui_Vgmax, ui_Vgmin, ui_Vgstep, ui_cycles, ui_Vd, id_limit, ig_limit, ui_sweepdelay):
        gp = GeneralParameters(sample, device, datadir, comments, "transfer")
        
        if ui_K2636:
            self.transfer_meas_instrument = K2636_GPIB(r'GPIB0::27')
        elif ui_U2722A:
            self.transfer_meas_instrument = U2722A_USB()
        else:
            self.transfer_meas_instrument = K2636_GPIB(r'GPIB0::27')
        

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
        tp.ins_k2636 = ui_K2636
        tp.ins_u2722a = ui_U2722A
        
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

    def RunOutput(self, sample, device, comments, datadir, ui_K2636, ui_U2722A, ui_Vg, ui_Vd_sweep_start, ui_Vd_sweep_stop, ui_Vd_sweep_step, ui_Vd_cyc_start, ui_Vd_cyc_max, ui_Vd_cyc_min, ui_Vd_cyc_step, ui_Vd_cycles, sweep_cyc, id_limit, ig_limit, ui_sweepdelay):
        gp = GeneralParameters(sample, device, datadir, comments, "output")
        
        if ui_K2636:
            self.output_meas_instrument = K2636_GPIB(r'GPIB0::27')
        elif ui_U2722A:
            self.output_meas_instrument = U2722A_USB()
        else:
            self.output_meas_instrument = K2636_GPIB(r'GPIB0::27')
        

        ### output characterization parameters
        op = Outputparameters()
        op.Vgs = ui_Vg
        op.sweep_cyc = sweep_cyc

        if sweep_cyc == 0 :
            op.Vds_start = ui_Vd_sweep_start
            op.Vds_end = ui_Vd_sweep_stop
            op.Vds_step = ui_Vd_sweep_step
        else:
            op.Vds_cyc_start = ui_Vd_cyc_start
            op.Vds_cyc_max = ui_Vd_cyc_max
            op.Vds_cyc_min = ui_Vd_cyc_min
            op.Vds_cyc_step = ui_Vd_cyc_step
            op.cycle_num = ui_Vd_cycles

        
        op.sweepDelay= ui_sweepdelay * 1e-03
        op.id_limit_ms = id_limit *1e-03 
        op.ig_limit_ms = ig_limit *1e-03
        op.ins_k2636 = ui_K2636
        op.ins_u2722a = ui_U2722A
        ###
        try:
            dl = datalogger(gp)
            # for transfers in range():
            self.output_characterizer = NANOBIO_OutputCharacterization(self.output_meas_instrument,op,dl) 
            self.output_characterizer.startMeasurement()
            print("processing Image")
            self.data_processor = processData(dl.filePath)
            self.data_processor.saveOutputCharacteristics()
            print('output characterization done ! ')
        except:
            print('something happened')
        self.output_meas_instrument.TurnoffChannels()

    def StopOutput(self):
        self.output_characterizer.measurementDone = True

    def runResistance (self, sample, device, comments, datadir, ui_K2636, ui_U2722A, ui_vdstart, ui_vdmax, ui_vdmin, ui_vdstep, ui_cycles, id_limit, ui_sweepdelay):
        gp = GeneralParameters(sample, device, datadir, comments, 'resistance')
        
        if ui_K2636:
            self.resistance_meas_instrument = K2636_GPIB(r'GPIB0::27')
        elif ui_U2722A:
            self.resistance_meas_instrument = U2722A_USB()
        else:
            self.resistance_meas_instrument = K2636_GPIB(r'GPIB0::27')

        ################# Channel Resistance  #################
        rp = ResistanceParameters()
        rp.Vds_Start = ui_vdstart
        rp.Vds_max = ui_vdmax
        rp.Vds_min = ui_vdmin
        rp.Vds_step = ui_vdstep
        rp.sweepDelay = ui_sweepdelay * 1e-03
        rp.number_of_res_meas = ui_cycles
        rp.id_limit_ms = id_limit *1e-03
        rp.ins_k2636 = ui_K2636
        rp.ins_u2722a = ui_U2722A
        
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

    def runImpedance (self, sample, device, comments, datadir, ui_oscamp, ui_startf, ui_stopf, ui_numofpoints, ui_electrodes, ui_solution, ui_BJT, ui_FET):
        gp = GeneralParameters(sample, device, datadir, comments, 'impedance')
        self.impedance_meas_instrument = SR7265(r'GPIB1::12::INSTR')
        
        ################## Impedance measurement ####################
        ip = ImpedanceParameters()
        ip.oscamp = ui_oscamp
        ip.startf = ui_startf
        ip.stopf = ui_stopf
        ip.numofpoints = ui_numofpoints
        ip.electrodes = ui_electrodes
        ip.solution = ui_solution
        ip.input_mode = 1
        if(ui_BJT.isChecked()):
            ip.input_mode = 0
        elif(ui_FET.isChecked()):
            ip.input_mode = 1
        try:
            dl = datalogger(gp)

            self.impedance_characterizer =  NANOBIO_impedance(self.impedance_meas_instrument,ip,dl)
            self.impedance_characterizer.startMeasurement()
            print("processing image")
            self.data_processor = processData(dl.filePath)
            self.data_processor.saveimpedance()
            print("impedance characterization done !")
        except:
            print('something happened')

    def StopImpedance(self):
        self.impedance_characterizer.measurementDone = True

    def runVoltammetery(self, sample ,  device , comments ,datadir, startV, endV, minV, scan_rate, step_size, cycles,I_limit):
        gp = GeneralParameters(sample, device, datadir, comments, 'cyclic_voltammetery')
        self.cyclic_voltammeter_instrument = K2636_CyclicVoltammeter(r'GPIB0::27')
        cvp = CyclicVoltammeteryParameters()
        cvp.startV = startV
        cvp.endV = endV
        cvp.minV = minV
        cvp.scan_rate = scan_rate * 1e-03 # now in mili
        cvp.step_size = step_size  * 1e-03 #now in mili
        cvp.cycles = cycles
        cvp.I_limit  = I_limit * 1e-03  # now this is in [mA]
        try:
            dl = datalogger(gp)
            self.cv_characterizer = NanoBIO_CVCharacterizer(self.cyclic_voltammeter_instrument, cvp, dl)
            self.cv_characterizer.startMeasurement()
            print("processing image")
            self.data_processor = processData(dl.filePath)
            self.data_processor.process_cyclic_voltammetery()
            print("cyclic voltammetery done")
        except: 
            print("exception in cyclic voltammetery")

    def StopVoltammery(self):
        self.cv_characterizer.measurementDone = True

    def runPotentiostat(self, sample, device , comments ,datadir, measurementDelay, measurementDuration, selectedChannel):
        if selectedChannel == 'SMU A':
            selectedChannel = 'smua'
        elif selectedChannel == 'SMU B':
            selectedChannel = 'smub'
        else:
            selectedChannel = 'smua'
        self.potentiostatInstrument = K2636_potentiostat(r'GPIB0::27', selectedChannel)
        gp = GeneralParameters(sample, device, datadir, comments, 'potentiostat')
        pp = PotentiostatParameters()
        pp.measurementDelay = measurementDelay
        pp.measurementDuration = measurementDuration
        try:
            dl = datalogger(gp)
            self.potential_characterizer = NanoBIO_PotentialCharacterizer(self.potentiostatInstrument, pp, dl)
            self.potential_characterizer.startMeasurement()
            print("processing image")
            self.data_processor = processData(dl.filePath)
            self.data_processor.process_potential_measurement()
            print("potential measurement done")
        except: 
            print("exception in potential measurement")

    def StopPotentialMeasurement(self):
        self.potential_characterizer.measurementDone = True