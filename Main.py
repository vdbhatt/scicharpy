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
        # self.Stop_general.clicked.connect(self.on_click_stopMeasure)
        self.Stop_online.clicked.connect(self.OnClickStopOnline)
        self.Stop_resistance.clicked.connect(self.OnClickStopResistance)
        self.Stop_transfer.clicked.connect(self.OnClickStopTransfer)
        self.browseFile.clicked.connect(self.open_file_path)
        defaultDir = r'C:\BioLab\Measurement Data'
        self.text_filepath.setText('{}'.format(defaultDir))
        self.characterization_system = TransistorCharacterizationTasks()
        

    @QtCore.pyqtSlot()
    def open_file_path(self):
        dataDir = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.text_filepath.setText('{}'.format(dataDir))

    @QtCore.pyqtSlot()
    def OnClickStartT(self):
        self.characterization_system.RunTransfer(self.text_sample.toPlainText(), self.text_device.toPlainText(), self.text_comments.toPlainText(), self.text_filepath.toPlainText(), self.Spinbox_Transfer_Vgstart.value(), self.Spinbox_Transfer_Vgmax.value(), self.Spinbox_Transfer_Vgmin.value(), self.Spinbox_Transfer_Vgstep.value(), self.Spinbox_Transfer_cycles.value(),self.Spinbox_Transfer_Vd.value(), self.spinbox_Id_limit.value(), self.spinbox_Ig_limit.value(), self.spinBox_DAQ.value())
    
    @QtCore.pyqtSlot()
    def OnClickStartR(self):
        self.characterization_system.runResistance(self.text_sample.toPlainText(), self.text_device.toPlainText(), self.text_comments.toPlainText(),self.text_filepath.toPlainText(), self.spinbox_res_Vdstart.value(), self.spinbox_res_Vdmax.value(), self.spinbox_res_Vdmin.value(), self.spinbox_res_Vdstep.value(), self.spinbox_res_cycles.value(), self.spinbox_Id_limit.value(), self.spinBox_DAQ.value())
    
    @QtCore.pyqtSlot()
    def OnClickStartO(self):
        self.characterization_system.runOnline(self.text_sample.toPlainText(), self.text_device.toPlainText(), self.text_comments.toPlainText(), self.text_filepath.toPlainText(), self.spinbox_vg.value(), self.spinbox_vd.value(), self.timeBSA.time(), self.timeProtein.time(), self.combo_BSA.currentText(), self.combo_protein.currentText(), self.spinbox_Id_limit.value(), self.spinbox_Ig_limit.value(), self.spinBox_DAQ.value(), self.proteinBSAtab.currentIndex())

    @QtCore.pyqtSlot()
    def OnClickStopOnline(self):
        self.characterization_system.StopOnline()

    @QtCore.pyqtSlot()
    def OnClickStopTransfer(self):
        self.characterization_system.StopTransfer()

    @QtCore.pyqtSlot()
    def OnClickStopResistance(self):
        self.characterization_system.StopResistance()


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainApplication()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()