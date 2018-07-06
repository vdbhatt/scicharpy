import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from DataProcessing.processData import *

datadir = r'C:\Users\data'
filename  = r'transfer'
processDataObject = processData(datadir, filename)
com, df = processDataObject.read_data_comments()
data = df.values
Vgs = data[:,0]
Vds = data[:,1]
Id = data[:,2]
Ig = data[:,3]
time = data[:,4]
##############################
# Id=[111,41,219,116,125,316,149,164,81,100]
# Vgs=[1,2,3,4,5,6,7,8,9,10]
# Ig=[1,2,3,4,5,6,7,8,9,10]
ydataf=[]
ydatab=[]
i=0
Vgsfrwd=[]
Idfrwd=[]
Vgsbck=[]
Idbck=[]

###############################


plt.plot(Vgs,Id)
print( GetIdIgRatio(Id, Ig) )


Vgs_max_ind=Vgs.argmax()

while(i<=Vgs_max_ind):
    Vgsfrwd.append(Vgs[i])
    Idfrwd.append(Id[i])
    i=i+1
i=i-1
while(i<len(Vgs)):
    Vgsbck.append(Vgs[i])
    Idbck.append(Id[i])
    i=i+1

Vgsbck = np.flip(Vgsbck,0)
Idbck = np.flip(Idbck,0)

Vthf,max_mf,cf= GetVth(Vgsfrwd, Idfrwd)
Vthb,max_mb,cb= GetVth(Vgsbck, Idbck)
print(Vthf,Vthb)

for number in Vgsfrwd:
    b=(max_mf*number)+cf
    if b>=0:
        ydataf.append(b)
    else:
        ydataf.append(0)
    
for number in Vgsbck:
    b=(max_mb*number)+cb
    if b>=0:
        ydatab.append(b)
    else:
        ydatab.append(0)

plt.plot(Vgsfrwd,ydataf,'y')
plt.plot(Vgsbck,ydatab,'g')
plt.show()

