import numpy as np

def poltocart(mag,phase):
    phaseinrad = (phase*np.pi)/180
    real = mag*np.cos(phaseinrad)
    img = mag*np.sin(phaseinrad)
    return real,img