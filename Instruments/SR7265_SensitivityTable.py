import numpy as np


def GetSensitivity():
    sensitivity_lookup = np.zeros(28)
    sensitivity_lookup[1] = 2e-09
    sensitivity_lookup[2] = 5e-09
    sensitivity_lookup[3] = 10e-09
    sensitivity_lookup[4] = 20e-09
    sensitivity_lookup[5] = 50e-09
    sensitivity_lookup[6] = 100e-09
    sensitivity_lookup[7] = 200e-09
    sensitivity_lookup[8] = 500e-09
    sensitivity_lookup[9] = 1e-06
    sensitivity_lookup[10] = 2e-06
    sensitivity_lookup[11] = 5e-06
    sensitivity_lookup[12] = 10e-06
    sensitivity_lookup[13] = 20e-06
    sensitivity_lookup[14] = 50e-06
    sensitivity_lookup[15] = 100e-06
    sensitivity_lookup[16] = 200e-06
    sensitivity_lookup[17] = 500e-06
    sensitivity_lookup[18] = 1e-03
    sensitivity_lookup[19] = 2e-03
    sensitivity_lookup[20] = 5e-03
    sensitivity_lookup[21] = 10e-03
    sensitivity_lookup[22] = 20e-03
    sensitivity_lookup[23] = 50e-03
    sensitivity_lookup[24] = 100e-03
    sensitivity_lookup[25] = 200e-03
    sensitivity_lookup[26] = 500e-03
    sensitivity_lookup[27] = 1

    return sensitivity_lookup
