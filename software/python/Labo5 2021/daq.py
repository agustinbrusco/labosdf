# NI-DAQmx Python Documentation: https://nidaqmx-python.readthedocs.io/en/latest/index.html
# NI USB-621x User Manual: https://www.ni.com/pdf/manuals/371931f.pdf
import matplotlib.pyplot as plt
import numpy as np
import nidaqmx
import math
import time


#para saber el ID de la placa conectada (DevX)
system = nidaqmx.system.System.local()
for device in system.devices:
    print(device)

## Medicion por tiempo/samples de una sola vez
def medir(duracion, fs):
    cant_puntos = duracion*fs    
    with nidaqmx.Task() as task:
        modo= nidaqmx.constants.TerminalConfiguration.DIFFERENTIAL
        task.ai_channels.add_ai_voltage_chan("Dev1/ai1", terminal_config = modo)
               
        task.timing.cfg_samp_clk_timing(fs,samps_per_chan = cant_puntos,
                                        sample_mode = nidaqmx.constants.AcquisitionType.FINITE)
        
        datos = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)           
    datos = np.asarray(datos)    
    return datos

duracion = 1 #segundos
fs = 250000 #Frecuencia de muestreo

y = medir(duracion, fs)
plt.plot(y)
plt.grid()
plt.show()


## Medicion continua
fs = 250000 #Frecuencia de muestreo
task = nidaqmx.Task()
modo= nidaqmx.constants.TerminalConfiguration.DIFFERENTIAL
task.ai_channels.add_ai_voltage_chan("Dev1/ai1", terminal_config = modo)
task.timing.cfg_samp_clk_timing(fs, sample_mode = nidaqmx.constants.AcquisitionType.CONTINUOUS)
task.start()
t0 = time.time()
total = 0
for i in range(10):
    time.sleep(0.1)
    datos = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)           
    total = total + len(datos)
    t1 = time.time()
    print("%2.3fs %d %d %2.3f" % (t1-t0, len(datos), total, total/(t1-t0)))    
task.stop()
task.close()

