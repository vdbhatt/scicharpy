import pandas as pd
import numpy as np
from io import StringIO 
import matplotlib.pyplot as plt
import os.path
import os
from scipy import stats

class processData():
    def __init__(self, dataFilepath):
        self.filepath_without_extension = os.path.splitext(dataFilepath)[0]
        self.filename = os.path.basename(dataFilepath)

        self.dataFilepath = dataFilepath 
        self.imagePath = self.filepath_without_extension + '.png'

    def read_data_comments(self, comment_symbol='#', sep=' '):
        dataLines = "".join([line for line in open(self.dataFilepath) 
                        if not ( line.startswith(comment_symbol) or line.startswith(' ') )])
        data = pd.read_csv(StringIO(dataLines), sep=sep, error_bad_lines=False)

        comments = "".join([line for line in open(self.dataFilepath) 
                        if (line.startswith(comment_symbol) and (not line.startswith(comment_symbol + 'header:')) )])
        return comments, data

    def saveTransferCharacteristics(self):
        com, df = self.read_data_comments()
        data = df.values
        Vgs = data[:,0]
        Vds = data[:,1]
        Id = data[:,2]
        Ig = data[:,3]
        time = data[:,4]
        titlestring = 'Transfer characteristics  ' + str(self.filename )


        Vth = 0 #self.GetVth(Vgs, Id)
        print(Vth)
        transferFigure = plt.figure()
        idaxis = transferFigure.add_subplot(111)
        Id_uA = Id/(1e-6)
        idaxis.plot(Vgs,Id_uA,'b')
        right = 1.1*np.max(Vgs)
        bottom = np.min(Id)

        idaxis.set_title(titlestring, fontsize=16)

        idaxis.set_xlabel(r'$V_{gs}[V]$', fontsize=20)
        idaxis.set_ylabel(r'$I_{d}[\mu A]$', color='b', fontsize=20)
        
        igaxis = idaxis.twinx()
        Ig_nA = Ig/(1e-9)
        igaxis.plot(Vgs,Ig_nA,'r')

        iglabel = igaxis.set_ylabel(r'$I_{g}[nA]$', color='r',fontsize=20)
        location = iglabel.get_position()
        
        igaxis.text(1.2, 0, com, fontsize=10, transform = igaxis.transAxes )
        idaxis.grid(True)        
        transferFigure.savefig(self.imagePath, dpi = 400, bbox_inches='tight')

    def GetVth (self, GateV, DrainI):
        '''
        this function will calculate the treshold of the transfer curve. 
        '''
        start_gate_value = GateV[0]
        max_gate_value = np.max(GateV)
        min_gate_value = np.min(GateV)
        diff = np.abs(GateV[0:] - start_gate_value)
        idxs = np.where(diff<0.0005)
        idxs = idxs[0]
        if (start_gate_value == max_gate_value) or (start_gate_value == min_gate_value):
            idxs = idxs[0::1]
        else:
            idxs = idxs[0::2]

        ############# average value of gateV and drainI ##############
        if len(idxs) == 2:
            gatev1 = np.array(GateV[idxs[0]:idxs[1]])
            gatev2 = np.array(GateV[idxs[1]:])
            if len(gatev1)==len(gatev2):
                gatev_array = np.array([gatev1,gatev2]).T
                avgtemp_gatev = np.mean(gatev_array, axis = 1)
                avg_gatev = np.reshape(avgtemp_gatev, (-1,1))
            else:
                avg_gatev = np.reshape(gatev1, (-1,1))
            
            draini1 = np.array(DrainI[idxs[0]:idxs[1]])
            draini2 = np.array(DrainI[idxs[1]:])
            if len(draini1)==len(draini2):
                draini_array = np.array([draini1,draini2]).T
                avgtemp_draini = np.mean(draini_array, axis=1)
                avg_draini = np.reshape(avgtemp_draini, (-1,1))
            else:
                avg_draini = np.reshape(draini1, (-1,1))
        
        elif len(idxs) == 3:
            gatev1 = np.array(GateV[idxs[0]:idxs[1]])
            gatev2 = np.array(GateV[idxs[1]:idxs[2]])
            gatev3 = np.array(GateV[idxs[2]:])
            if len(gatev1)==len(gatev2) and len(gatev2)==len(gatev3):
                gatev_array = np.array([gatev1,gatev2,gatev3]).T
                avgtemp_gatev = np.mean(gatev_array, axis=1)
                avg_gatev = np.reshape(avgtemp_gatev, (-1,1))
            elif len(gatev1)==len(gatev2) and len(gatev2) != len(gatev3):
                gatev_array = np.array([gatev1,gatev2]).T
                avgtemp_gatev = np.mean(gatev_array, axis=1)
                avg_gatev = np.reshape(avgtemp_gatev, (-1,1))
            else:
                avg_gatev = np.reshape(gatev1, (-1,1))

            draini1 = np.array(DrainI[idxs[0]:idxs[1]])
            draini2 = np.array(DrainI[idxs[1]:idxs[2]])
            draini3 = np.array(DrainI[idxs[2]:])
            if len(draini1)==len(draini2) and len(draini2)==len(draini3):
                draini_array = np.array([draini1,draini2,draini3]).T
                avgtemp_draini = np.mean(draini_array, axis=1)
                avg_draini = np.reshape(avgtemp_draini, (-1,1))
            elif len(draini1)==len(draini2) and len(draini2)!=len(draini3):
                draini_array = np.array([draini1,draini2]).T
                avgtemp_draini = np.mean(draini_array, axis=1)
                avg_draini = np.reshape(avgtemp_draini, (-1,1))
            else:
                avg_draini = np.reshape(draini1, (-1,1))
        
        else:
            gatev1 = np.array(GateV[idxs[0]:])
            avg_gatev = np.reshape(gatev1, (-1,1))

            draini1 = np.array(DrainI[idxs[0]:])
            avg_draini = np.reshape(draini1, (-1,1))

        ########### Vth calculation ###############

        min_gatev = np.amin(avg_gatev) #minimum value of gate voltage (where drain I is highest)
        idxmax = np.where(avg_gatev == min_gatev) #returns index of min gate value
        idxmax = np.asscalar(idxmax[0])

        #compute gradient of DrainI, to get the point steepest point of the curve
        gradcurr_fw = np.gradient(avg_draini[0:idxmax],axis=0,edge_order=2)
        maxgrad_fw = np.amax(abs(gradcurr_fw))
        maxgrad_idx = np.where(abs(gradcurr_fw) == maxgrad_fw)
        maxgrad_idx = np.asscalar(maxgrad_idx[0])


        points_around_gm = 5
        points_to_add = 5
        while True: 
            try:
                line_x = avg_gatev[maxgrad_idx - points_around_gm : maxgrad_idx + points_around_gm]
                line_y = avg_draini[maxgrad_idx - points_around_gm : maxgrad_idx + points_around_gm]
                slope, intercept, r_value, p_value, std_err = stats.linregress(line_x[:,0],line_y[:,0])
                confidence = r_value**2
                if (confidence > 0.96):
                    break   
                points_around_gm += points_to_add
            except ValueError:
                points_around_gm -=6
                points_to_add -= 1
                

        fitting_line_xpoints = np.linspace(0, min_gatev, 100)
        fitting_line = slope*fitting_line_xpoints + intercept
        Vth = -intercept/slope

        return Vth

    def saveOutputCharacteristics(self):
        com, df = self.read_data_comments()
        data = df.values
        Vgs = data[:,0]
        Vds = data[:,1]
        Id = data[:,2]
        Ig = data[:,3]
        time = data[:,4]
        titlestring = 'Output characteristics  ' + str(self.filename )

        outputFigure = plt.figure()
        idaxis = outputFigure.add_subplot(111)
        Id_uA = Id/(1e-6)
        idaxis.plot(Vds,Id_uA,'b')
        right = 1.1*np.max(Vds)
        bottom = np.min(Id)

        idaxis.set_title(titlestring, fontsize=16)

        idaxis.set_xlabel(r'$V_{ds}[V]$', fontsize=20)
        idaxis.set_ylabel(r'$I_{d}[\mu A]$', color='b', fontsize=20)
        
        igaxis = idaxis.twinx()
        Ig_nA = Ig/(1e-9)
        igaxis.plot(Vds,Ig_nA,'r')

        iglabel = igaxis.set_ylabel(r'$I_{g}[nA]$', color='r',fontsize=20)
        location = iglabel.get_position()
        
        igaxis.text(1.2, 0, com, fontsize=10, transform = igaxis.transAxes )
        idaxis.grid(True)        
        outputFigure.savefig(self.imagePath, dpi = 400, bbox_inches='tight')


    def saveResistanceCharacteristics(self):
        com, df = self.read_data_comments()
        data = df.values
        Vds = data[:,0]
        Id = data[:,1]
        time = data[:,2]
        titlestring = 'Resistance characteristics  ' + str(self.filename )

        resFigure = plt.figure()
        idaxis = resFigure.add_subplot(111)
        Id_uA = Id/(1e-6)
        idaxis.plot(Vds,Id_uA,'b')

        idaxis.set_title(titlestring, fontsize=20)

        idaxis.set_xlabel(r'$V_{ds}[V]$', fontsize=20)
        idaxis.set_ylabel(r'$I_{d}[\mu A]$', color='b', fontsize=20)
        right = 1.2*np.max(Vds)
        bottom = np.min(Id)
        idaxis.text(right, bottom, com, fontsize=10, transform = idaxis.transAxes )
        idaxis.grid(True)
        
        resFigure.savefig(self.imagePath, dpi = 400, bbox_inches='tight')
    
    def saveimpedance(self):
        com, df = self.read_data_comments()
        data = df.values
        freq = data[:,0]
        real = data[:,1]
        imag = data[:,2]
        titlestring = str(self.filename )

        resFigure = plt.figure(figsize=(6,6))
        imp_axis = resFigure.add_subplot(111)
       
        xwidth = np.amax(real)-np.amin(real)
        ywidth = np.amax(imag)-np.amin(imag)
        width = np.amax([xwidth, ywidth])

        xedge = np.amax(real)*0.1
        yedge = np.amax(imag)*0.1
        edge= np.amax([xedge, yedge])
        ymin = np.amin(imag)-edge
        ytop = np.amin(imag) + width + edge
        xmin = np.amin(real)-edge
        xtop = np.amin(real) + width + edge
       
        
        imp_axis.set_xlim(xmin, xtop)
        imp_axis.set_ylim(ymin, ytop)
        imp_axis.plot(real, imag, '*')

        imp_axis.set_title(titlestring, fontsize=20)

        imp_axis.set_xlabel(r'$Z_{real}[\Omega]$', color='b', fontsize=20)
        imp_axis.set_ylabel(r'$-Z_{imag}[\Omega]$', color='b', fontsize=20)
        right = 1 
        bottom = 0 

        imp_axis.text(right, bottom, com, fontsize=10, transform = imp_axis.transAxes )
        imp_axis.grid(True)
        resFigure.savefig(self.imagePath, dpi = 400, bbox_inches='tight')

    def process_cyclic_voltammetery(self):
        com, df = self.read_data_comments()
        data = df.values
        V = data[:,0]
        I = data[:,1]
        titlestring = str(self.filename )

        resFigure = plt.figure(figsize=(6,6))
        imp_axis = resFigure.add_subplot(111)
        imp_axis.plot(V, I, '*')

        imp_axis.set_title(titlestring, fontsize=20)

        imp_axis.set_xlabel(r'$V[V]$', color='b', fontsize=20)
        imp_axis.set_ylabel(r'$I[I]$', color='b', fontsize=20)
        right = 1 
        bottom = 0
        imp_axis.text(right, bottom, com, fontsize=10, transform = imp_axis.transAxes )
        imp_axis.grid(True)
        resFigure.savefig(self.imagePath, dpi = 400, bbox_inches='tight')        

    def process_potential_measurement(self):
        com, df = self.read_data_comments()
        data = df.values
        V = data[:,0]
        t = data[:,1]
        titlestring = str(self.filename )

        resFigure = plt.figure(figsize=(6,6))
        imp_axis = resFigure.add_subplot(111)
        imp_axis.plot(t, V, '*')

        imp_axis.set_title(titlestring, fontsize=20)

        imp_axis.set_xlabel(r'$V[V]$', color='b', fontsize=20)
        imp_axis.set_ylabel(r'$I[I]$', color='b', fontsize=20)
        right = 1 
        bottom = 0
        imp_axis.text(right, bottom, com, fontsize=10, transform = imp_axis.transAxes )
        imp_axis.grid(True)
        resFigure.savefig(self.imagePath, dpi = 400, bbox_inches='tight')   


    def saveOnlineCharacteristics(self):
        com, df = self.read_data_comments()
        data = df.values
        Vds = data[:,0]
        Id = data[:,2]
        Ig=data[:,3]
        time = data[:,4]
        titlestring = 'Online Current Measurement  ' + str(self.filename )

        CurrmeasFigure = plt.figure()
        idaxis = CurrmeasFigure.add_subplot(111)
        Id_uA = Id/(1e-6)
        idaxis.plot(time,Id_uA,'b')

        idaxis.set_title(titlestring, fontsize=20)

        idaxis.set_xlabel(r'$Time_{s}$', fontsize=20)
        idaxis.set_ylabel(r'$I_{d}[\mu A]$', color='b', fontsize=20)
        right = 1.2*np.max(Vds)
        bottom = np.min(Id)
        idaxis.text(right, bottom, com, fontsize=10, transform = idaxis.transAxes )
        idaxis.grid(True)
        CurrmeasFigure.savefig(self.imagePath, dpi = 400, bbox_inches='tight')

    def saveOnlinefor2terminaltransistor(self):
        com, df = self.read_data_comments()
        data = df.values
        Id = data[:,1]
        time = data[:,2]
        titlestring = 'Online CurrentvsTime Measurement 2terminal  ' + str(self.filename )

        CurrmeasFigure = plt.figure()
        idaxis = CurrmeasFigure.add_subplot(111)
        Id_uA = Id/(1e-6)
        idaxis.plot(time,Id_uA,'b')

        idaxis.set_title(titlestring, fontsize=20)

        idaxis.set_xlabel(r'$Time_{s}$', fontsize=20)
        idaxis.set_ylabel(r'$I_{d}[\mu A]$', color='b', fontsize=20)
        right = 1.2*np.max(commonvoltage)
        bottom = np.min(Id)
        idaxis.text(right, bottom, com, fontsize=10, transform = idaxis.transAxes )
        idaxis.grid(True)
        CurrmeasFigure.savefig(self.imagePath, dpi = 400, bbox_inches='tight')