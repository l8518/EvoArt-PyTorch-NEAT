import math
import numpy as np
import sounddevice as sd

block_duration = 50
device = None
samplerate = sd.query_devices(device, 'input')['default_samplerate']

def callback(indata, frames, time, status):
    if status:
        print(status)
    if any(indata):
        # magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
        print("some audio input 😎")
    else:
        print('no input')


with sd.InputStream(device=device, channels=1, callback=callback,
                    blocksize=int(samplerate * block_duration / 1000),
                    samplerate=samplerate):
    while True:
        response = input()
