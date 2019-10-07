import math
import numpy as np
import sounddevice as sd

device = None
samplerate = sd.query_devices(device, 'input')['default_samplerate']  # sample rate per second
block_duration = 100 # blocksize in milliseconds
block_size = int(samplerate * block_duration / 1000)
low, high = [100, 2000]
freqbands_n = 12
delta_f = (high - low) / (freqbands_n - 1)
fftsize = math.ceil(samplerate / delta_f)
low_bin = math.floor(low / delta_f)

def callback(inputdata, frames, time, status):
    if status:
        print(status)
    if any(inputdata):
        magnitude = np.abs(np.fft.rfft(inputdata[:, 0], n=fftsize))
        magnitude *= 10 / fftsize  # normalize
        intensity_band = [np.clip(x, 0, 1) for x in magnitude[low_bin:low_bin + freqbands_n]]
        print(intensity_band)

    else:
        print('no audio input fetched')


with sd.InputStream(device=device, channels=1, callback=callback,
                    blocksize=block_size,
                    samplerate=samplerate):
    while True:
        response = input()
