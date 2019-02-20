import numpy as np
import pandas as pd
import os.path
import fnmatch
import os
import arrow

class datalogger():
    def __init__(self,gp):

        measDate = arrow.now().format('YYYY-MM-DD')
        self.filename  = gp.type + measDate + r'S#'+gp.sampleName + r'_D#' +gp.deviceName
        self.filePath = os.path.join(os.path.sep, gp.dataDir,self.filename + '.csv')
        # if file already exists with the given name make a new file with # and increase
        # file number 
        # for e.g if file abc exists then make abc#1 
        # if abc, abc#1 exists then make abc#2 etc..
        if( os.path.isfile(self.filePath)):
            existing_file_count = self.find_files()
            if existing_file_count > 0:
                self.filename = self.filename + '_run#' +str(existing_file_count + 1 )
                self.filePath = os.path.join(os.path.sep, gp.dataDir, self.filename + '.csv')
        # if gp.measCond != None:
        #     f = open(self.filePath , 'a')
        #     f.write(gp.measCond + '\n')
        #     f.close()
        self.measCond = gp.measCond

    def WriteMeasurementSettings(self,settings):
            f = open(self.filePath , 'a')
            f.write(settings + '\n')
            f.close()

    def find_files(self):
        '''Return list of files matching pattern in base folder.'''
        baseFolder = os.path.dirname(self.filePath)
        filenameWithExtension = os.path.basename(self.filePath)
        filename = os.path.splitext(filenameWithExtension)[0]
        matchingfiles = 0
        for file in os.listdir(baseFolder):
            if filename in file:
                if '.csv' in file:
                    matchingfiles +=  1
        return matchingfiles

    def saveTransfer( self, Id,Ig,Vds,Vgs,timestep):
        Id_np = np.array(Id)
        Ig_np = np.array(Ig)
        Vds_np = np.array(Vds)
        Vgs_np = np.array(Vgs)
        time_np = np.array(timestep)
        rows = Id_np.shape[0]
        data = np.zeros(rows*5).reshape(rows,5)
        data[:,0] = Vgs_np
        data[:,1] = Vds_np
        data[:,2] = Id_np
        data[:,3] = Ig_np
        data[:,4] = time_np
        f = open(self.filePath, 'a')
        f.write('\n#  Vgs  Vds  Id  Ig  timestamp' + '\n')
        f.close()
        self.saveData(data)

    def saveOutput(self, Id,Ig,Vds,Vgs,timestep):
        Id_np = np.array(Id)
        Ig_np = np.array(Ig)
        Vds_np = np.array(Vds)
        Vgs_np = np.array(Vgs)
        time_np = np.array(timestep)
        rows = Id_np.shape[0] 
        data = np.zeros(rows*5).reshape(rows,5)
        data[:,0] = Vgs_np
        data[:,1] = Vds_np
        data[:,2] = Id_np
        data[:,3] = Ig_np
        data[:,4] = time_np
        f = open(self.filePath, 'a')
        f.write('\n#  Vgs  Vds  Id  Ig  timestamp' + '\n')
        f.close()
        self.saveData(data)


    def saveResistance(self, Id, VdsBuffer, timestamp):
        vds_np = np.array(VdsBuffer)
        Id_np = np.array(Id)
        time_np = np.array(timestamp)
        rows = Id_np.shape[0]
        data = np.zeros(rows*5).reshape(rows,5)
        data[:,0] = vds_np
        data[:,1] = Id_np
        data[:,2] = time_np

        f = open(self.filePath, 'a')
        f.write('\n#  Vds  Id  timestamp' + '\n')
        f.close()
        self.saveData(data)
    
    def saveImpedance(self, frequency, Zreal, Zimag, rawmeasurement, timestamp):
        frequency_np = np.array(frequency)
        Zreal_np = np.array(Zreal)
        Zimag_np = np.array(Zimag)
        iter = 0
        rows = frequency_np.shape[0]
        data = np.zeros(rows*6).reshape(rows,6)
        timestamp_np = np.array(timestamp)
        data[:,0] = frequency_np
        data[:,1] = Zreal_np
        data[:,2] = Zimag_np
        for meas in rawmeasurement:
            rawmeasurement_mag_volts_np = np.array(float(meas.split(',')[0]))
            rawmeasurement_phase_degree_np = np.array(float(meas.split(',')[1]))       
            data[iter,3] = rawmeasurement_mag_volts_np
            data[iter,4] = rawmeasurement_phase_degree_np
            iter += 1
        data[:,5] = timestamp_np
        f = open(self.filePath, 'a')
        f.write('\n#header:  frequency, Zreal, -Zimag, rawmeasurement_mag_volts, rawmeasurement_phase_degree, timestamp' + '\n')
        f.close()
        self.saveData(data)

    def save_cyclic_voltammetery(self, V, I, timestamp):
        V_np = np.array(V)
        I_np = np.array(I)
        timestamp_np = np.array(timestamp)
        rows = timestamp_np.shape[0]
        data = np.zeros(rows*3).reshape(rows,3)
        data[:,0] = V_np
        data[:,1] = I_np
        data[:,2] = timestamp_np
        f = open(self.filePath, 'a')
        f.write('\n#  Volt, Current, timestamp' + '\n')
        f.close()
        self.saveData(data)

    def save_potential_measurement(self, V, timestamp):
        V_np = np.array(V)
        timestamp_np = np.array(timestamp)

        rows = timestamp_np.shape[0]
        data = np.zeros(rows*2).reshape(rows,2)
        data[:,0] = V_np
        data[:,1] = timestamp_np
        f = open(self.filePath, 'a')
        f.write('\n#  Volt, timestamp' + '\n')
        f.close()
        self.saveData(data)

    def saveOnline_Measurement(self, Id,Ig,Vds,Vgs,timestep):
        Id_sp = np.array(Id)
        Ig_sp = np.array(Ig)
        Vds_sp = np.array(Vds)
        Vgs_sp = np.array(Vgs)
        time_sp = np.array(timestep)
        rows = Id_sp.shape[0] 
        data = np.zeros(rows*5).reshape(rows,5)
        data[:,0] = Vgs_sp
        data[:,1] = Vds_sp
        data[:,2] = Id_sp
        data[:,3] = Ig_sp
        data[:,4] = time_sp
        f = open(self.filePath, 'a')
        f.write('\n#  Vgs  Vds  Id  Ig  timestamp' + '\n')
        f.close()
        self.saveData(data)

    def append_OnlineData(self, measured_Id, measured_Ig, Vds, Vgs, measurementTime):
        
        data = np.zeros(5).reshape(1,5)
        data[:,0] = Vgs
        data[:,1] = Vds
        data[:,2] = measured_Id
        data[:,3] = measured_Ig
        data[:,4] = measurementTime
        self.saveData(data)

    def append_Onlinedatatwoterminal(self,measured_Id,commonvoltage,measurementTime):
        Id_twotp = np.array(measured_Id)
        commonvoltage_twotp = np.array(commonvoltage)
        time_twotp = np.array(measurementTime) 
        data = np.zeros(3).reshape(1,3)
    
        data[:,0] = commonvoltage_twotp
        data[:,1] = Id_twotp
        data[:,2] = time_twotp
        self.saveData(data)

    def append_OnlinePotentialMeas(self, measured_VA,measured_VB, measurementTime):
        data = np.zeros(3).reshape(1,3)
        data[:,0] = measured_VA
        data[:,1] = measured_VB
        data[:,2] = measurementTime
        self.saveData(data)

    def saveData(self, data):
        dataframe = pd.DataFrame(data=data.astype(float))
        self.wait_for_files()
        dataframe.to_csv(self.filePath, mode='a', sep=' ', header=False, float_format='%.15f', index=False)

    def is_locked(self):
        locked = None
        file_object = None
        if os.path.exists(self.filePath):
            try:
                buffer_size = 8
                # Opening file in append mode and read the first 8 characters.
                file_object = open(self.filePath, 'a', buffer_size)
                if file_object:
                    locked = False
            except:
                locked = True
            finally:
                if file_object:
                    file_object.close()
        else:
            print( "file not found.")
        return locked

    def wait_for_files(self):
        wait_time = 0.1
        while self.is_locked():
            print ("file is currently in use. Waiting to close")
            time.sleep(wait_time)