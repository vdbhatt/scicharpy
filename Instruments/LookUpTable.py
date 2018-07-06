def GetTimeConstantLUT():
    
    time_const_lookup = np.zeros(30)
    time_const_lookup[0] = 10e-6
    time_const_lookup[1] = 20e-6
    time_const_lookup[2] = 40e-6
    time_const_lookup[3] = 80e-6
    time_const_lookup[4] = 160e-6
    time_const_lookup[5] = 320e-6
    time_const_lookup[6] = 640e-6
    time_const_lookup[7] = 5e-3
    time_const_lookup[8] = 10e-3
    time_const_lookup[9] = 20e-3
    time_const_lookup[10] = 50e-3
    time_const_lookup[11] = 100e-3
    time_const_lookup[12] = 200e-3
    time_const_lookup[13] = 500e-3
    time_const_lookup[14] = 1
    time_const_lookup[15] = 2
    time_const_lookup[16] = 5
    time_const_lookup[17] = 10
    time_const_lookup[18] = 20
    time_const_lookup[19] = 50
    time_const_lookup[20] = 100
    time_const_lookup[21] = 200
    time_const_lookup[22] = 500
    time_const_lookup[23] = 1000
    time_const_lookup[24] = 2000
    time_const_lookup[25] = 5000
    time_const_lookup[26] = 10000
    time_const_lookup[27] = 20e3
    time_const_lookup[28] = 50e3
    time_const_lookup[29] = 100e3

    return time_const_lookup

import numpy as np
start_f = 1 # in hertz 
stop_f = 50000 # in hertz
log_stop_f =  np.log10(stop_f)
print(log_stop_f)
freq_array  = np.logspace(np.log10(start_f),log_stop_f, num=10)



correct_time_constant = 29
time_to_wait_for_stable_signal = 100e3

time_const_lookup = GetTimeConstantLUT()  

for freq in freq_array:
    time_period = 5.0/freq
    for timeconstant in time_const_lookup:
        if time_period < timeconstant :
            correct_time_constant = np.where(time_const_lookup == timeconstant )
            time_to_wait_for_stable_signal = time_period
            break
    print(freq)
    # print(time_period)
    # print('time const index %s' %correct_time_constant )
    # print('sleeping for %s ' %time_to_wait_for_stable_signal)
    # print(' measuring now.. ')
    
