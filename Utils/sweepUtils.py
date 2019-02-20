import numpy as np

def GetSweepVoltage(startV, endV, stepsize):
    """
    returns array of voltages if given start end and stepsize 
    """   
    startV = startV
    endV = endV
    stepsize = abs(stepsize)
    varray = []
    vstep = startV
    varray.append(vstep)
    if startV < endV:  
        while(vstep <= endV):
            vstep += stepsize
            varray.append(vstep)
    else:
        while(vstep >= endV):
            vstep -= stepsize
            varray.append(vstep)
    return varray

def GetDoubleSweep(startV, maxV, minV, stepsize, number_of_transfer_meas):

    if startV > maxV:
        raise Exception('wrong parameters')
    if minV > maxV:
        raise Exception('wrong parameters')
    if minV > startV:
        raise Exception('wrong parameters')
    
    i = 0
    step=abs(stepsize)
    while step < 1 :
        step = step * 10
        i += 1

    k = 10**i
    startV_k = startV * k
    maxV_k = maxV * k
    minV_k = minV * k

    if stepsize < 0 :
        number_points1 = int((abs(startV_k-minV_k)/step))
        number_points2 = int((abs(minV_k-maxV_k)/step))
        number_points3 = int((abs(maxV_k-startV_k)/step))
        int1 = np.linspace(startV_k, minV_k, number_points1, endpoint=False)/k
        int2 = np.linspace(minV_k, maxV_k, number_points2, endpoint=False)/k
        int3 = np.linspace(maxV_k, startV_k, number_points3, endpoint=False)/k
    else : 
        number_points1 = int((abs(startV_k-maxV_k)/step))
        number_points2 = int((abs(maxV_k-minV_k)/step))
        number_points3 = int((abs(minV_k-startV_k)/step))
        int1 = np.linspace(startV_k, maxV_k, number_points1, endpoint=False)/k
        int2 = np.linspace(maxV_k, minV_k, number_points2, endpoint=False)/k
        int3 = np.linspace(minV_k, startV_k, number_points3, endpoint=False)/k
    varray= []

    for count in range(number_of_transfer_meas):
        varray = np.append(varray,int1)
        varray = np.append(varray,int2)
        varray = np.append(varray,int3)

    varray = np.append(varray,startV)
    return varray