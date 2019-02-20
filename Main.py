import sys
from PyQt5 import QtCore, QtGui, QtWidgets


from UI.MainUI import *
from CharacterizationType.Characterization import * 

class MainApplication(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainApplication, self).__init__(parent)
        self.setupUi(self)
        self.Start_transfer.clicked.connect(self.OnClickStartT)
        self.Start_resistance.clicked.connect(self.OnClickStartR)
        self.Start_online.clicked.connect(self.OnClickStartO)
        self.Start_impedance.clicked.connect(self.OnClickStartI)
        # self.Start_general.clicked.connect(self.OnClickStartG)
        # self.Stop_general.clicked.connect(self.OnClickStopG)
        self.Start_output.clicked.connect(self.OnClickStartOut)
        self.Stop_output.clicked.connect(self.OnClickStopOut)
        self.Stop_online.clicked.connect(self.OnClickStopOnline)
        self.Stop_resistance.clicked.connect(self.OnClickStopResistance)
        self.Stop_transfer.clicked.connect(self.OnClickStopTransfer)
        self.Stop_impedance.clicked.connect(self.OnClickStopI) 
        self.browseFile.clicked.connect(self.open_file_path)
        self.start_voltammetry.clicked.connect(self.OnclickstartV)
        self.stop_voltammetry.clicked.connect(self.OnclickstopV)
        self.start_potentialMeas.clicked.connect(self.OnClickStartPotentiostat)
        self.stop_potentialMeas.clicked.connect(self.OnClickStopPotentiostat)
        self.Pause_online.clicked.connect(self.OnClickPauseO)
        self.Continue_online.clicked.connect(self.OnClickContinueO)
        self.Update_online.clicked.connect(self.OnClickUpdateO)
        
        defaultDir = r'C:\Users\'
        self.text_filepath.setText('{}'.format(defaultDir))
        self.characterization_system = TransistorCharacterizationTasks()

    @QtCore.pyqtSlot()
    def open_file_path(self):
        dataDir = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.text_filepath.setText('{}'.format(dataDir))


    # @QtCore.pyqtSlot()
    # def OnClickStartG(self):
    #     self.characterization_system.RunGeneral()
    
    @QtCore.pyqtSlot()
    def OnClickStartT(self):
        self.characterization_system.RunTransfer(self.text_sample.toPlainText(), self.text_device.toPlainText(), self.text_comments.toPlainText(), self.text_filepath.toPlainText(), self.radioButton_mu_k2636.isChecked(), self.radioButton_mu_u2722a.isChecked(), self.Spinbox_Transfer_Vgstart.value(), self.Spinbox_Transfer_Vgmax.value(), self.Spinbox_Transfer_Vgmin.value(), self.Spinbox_Transfer_Vgstep.value(), self.Spinbox_Transfer_cycles.value(),self.Spinbox_Transfer_Vd.value(), self.spinbox_Id_limit.value(), self.spinbox_Ig_limit.value(), self.spinBox_DAQ.value())
    
    @QtCore.pyqtSlot()
    def OnClickStartOut(self):
        self.characterization_system.RunOutput(self.text_sample.toPlainText(), self.text_device.toPlainText(), self.text_comments.toPlainText(), self.text_filepath.toPlainText(), self.radioButton_mu_k2636.isChecked(), self.radioButton_mu_u2722a.isChecked(), self.Spinbox_output_Vg.value(), self.output_sweep_start_vd.value(), self.output_sweep_stop_vd.value(), self.output_sweep_step_vd.value(), self.output_cyc_start_vd.value(), self.output_cyc_max_vd.value(), self.output_cyc_min_vd.value(), self.output_cyc_step_vd.value(), self.output_cycnum_vd.value(), self.Vd_tab.currentIndex(), self.spinbox_Id_limit.value(), self.spinbox_Ig_limit.value(), self.spinBox_DAQ.value())

    @QtCore.pyqtSlot()
    def OnClickStartR(self):
        self.characterization_system.runResistance(self.text_sample.toPlainText(), self.text_device.toPlainText(), self.text_comments.toPlainText(),self.text_filepath.toPlainText(), self.radioButton_mu_k2636.isChecked(), self.radioButton_mu_u2722a.isChecked(), self.spinbox_res_Vdstart.value(), self.spinbox_res_Vdmax.value(), self.spinbox_res_Vdmin.value(), self.spinbox_res_Vdstep.value(), self.spinbox_res_cycles.value(), self.spinbox_Id_limit.value(), self.spinBox_DAQ.value())
    
    @QtCore.pyqtSlot()
    def OnClickStartO(self):
        self.characterization_system.runOnline(self.text_sample.toPlainText(), self.text_device.toPlainText(), self.text_comments.toPlainText(), self.text_filepath.toPlainText(), self.radioButton_mu_k2636.isChecked(), self.radioButton_mu_u2722a.isChecked(), self.radio_gate_DC.isChecked(), self.radio_gate_AC.isChecked(), self.spinbox_vg.value(), self.spinbox_vd.value(), self.timeBSA.time(), self.timeProtein.time(), self.timeIon.time(), self.check_BSAtime.isChecked(), self.check_proteintime.isChecked(), self.check_iontime.isChecked(), self.combo_BSA.currentText(), self.combo_protein.currentText(), self.text_ions.toPlainText(), self.spinbox_Id_limit.value(), self.spinbox_Ig_limit.value(), self.spinBox_DAQ.value(), self.proteinBSAtab.currentIndex(), self.check_vg_turnoff.isChecked(), self.check_vd_turnoff.isChecked())

    @QtCore.pyqtSlot()
    def OnClickStartI(self):
        self.characterization_system.runImpedance(self.text_sample.toPlainText(), self.text_device.toPlainText(), self.text_comments.toPlainText(), self.text_filepath.toPlainText(), self.doubleSpin_oscamp.value(), self.doubleSpin_startf.value(), self.doubleSpin_stopf.value(), self.spinBox_num.value(), self.text_electrodes.toPlainText(), self.text_solution.toPlainText(), self.radioButton_BJT, self.radioButton_FET)

    @QtCore.pyqtSlot()
    def OnclickstartV(self):
        self.characterization_system.runVoltammetery(self.text_sample.toPlainText(), self.text_device.toPlainText(), self.text_comments.toPlainText(), self.text_filepath.toPlainText(), self.doubleSpinBox_startV.value(), self.doubleSpinBox_endV.value(), self.doubleSpinBox_minV.value(), self.doubleSpinBox_scan_rate.value(),   self.doubleSpinBox_step_size.value(), self.spinBox_cycles.value(), self.spinbox_I_limit.value() )
  
    @QtCore.pyqtSlot()
    def OnClickStartPotentiostat(self):
        self.characterization_system.runPotentiostat(self.text_sample.toPlainText(), self.text_device.toPlainText(), self.text_comments.toPlainText(), self.text_filepath.toPlainText(), self.doubleSpinBox_measDelay.value(), self.doubleSpinBox_measurementDuration.value(), self.comboBox_potentiostatChannel.currentText())

    # @QtCore.pyqtSlot()
    # def OnClickStopG(self):
    #     self.characterization_system.StopGeneral()

    @QtCore.pyqtSlot()
    def OnclickstopV(self):
        self.characterization_system.StopVoltammery()

    @QtCore.pyqtSlot()
    def OnClickStopOnline(self):
        self.characterization_system.StopOnline()

    @QtCore.pyqtSlot()
    def OnClickPauseO(self):
        self.characterization_system.PauseOnline()

    @QtCore.pyqtSlot()
    def OnClickContinueO(self):
        self.characterization_system.ContinueOnline()

    @QtCore.pyqtSlot()
    def OnClickUpdateO(self):
        self.characterization_system.UpdateOnline(self.text_sample.toPlainText(), self.text_device.toPlainText(), self.text_comments.toPlainText(), self.text_filepath.toPlainText(), self.radioButton_mu_k2636.isChecked(), self.radioButton_mu_u2722a.isChecked(), self.radio_gate_DC.isChecked(), self.radio_gate_AC.isChecked(), self.spinbox_vg.value(), self.spinbox_vd.value(), self.timeBSA.time(), self.timeProtein.time(), self.timeIon.time(), self.check_BSAtime.isChecked(), self.check_proteintime.isChecked(), self.check_iontime.isChecked(), self.combo_BSA.currentText(), self.combo_protein.currentText(), self.text_ions.toPlainText(), self.spinbox_Id_limit.value(), self.spinbox_Ig_limit.value(), self.spinBox_DAQ.value(), self.proteinBSAtab.currentIndex(), self.check_vg_turnoff.isChecked(), self.check_vd_turnoff.isChecked())

    @QtCore.pyqtSlot()
    def OnClickStopTransfer(self):
        self.characterization_system.StopTransfer()

    @QtCore.pyqtSlot()
    def OnClickStopOut(self):
        self.characterization_system.StopOutput()

    @QtCore.pyqtSlot()
    def OnClickStopResistance(self):
        self.characterization_system.StopResistance()

    @QtCore.pyqtSlot()
    def OnClickStopI(self):
        self.characterization_system.StopImpedance()  

    @QtCore.pyqtSlot()
    def OnClickStopPotentiostat(self):
        self.characterization_system.StopPotentialMeasurement()  
        



def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainApplication()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()