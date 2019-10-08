import math
import numpy as np
import sounddevice as sd
from concurrent.futures import ThreadPoolExecutor


class AudioPreprocessor(object):
    def __init__(self, freq_bands):
        self.device = None
        self.samplerate = sd.query_devices(self.device, 'input')['default_samplerate']  # sample rate per second
        self.block_duration = 100  # blocksize in milliseconds
        self.block_size = int(self.samplerate * self.block_duration / 1000)
        self.low, self.high = [100, 2000]
        self.freqbands_n = freq_bands
        self.delta_f = (self.high - self.low) / (self.freqbands_n - 1)
        self.fftsize = math.ceil(self.samplerate / self.delta_f)
        self.low_bin = math.floor(self.low / self.delta_f)
        self.current_intensity_band = [0 for i in range(self.freqbands_n)]

    def callback(self, inputdata, frames, time, status):
        if status:
            print(status)
        if any(inputdata):
            magnitude = np.abs(np.fft.rfft(inputdata[:, 0], n=self.fftsize))
            magnitude *= 10 / self.fftsize  # normalize
            low_bin = self.low_bin
            intensity_band = [np.clip(x, 0, 1) for x in magnitude[low_bin:low_bin + self.freqbands_n]]
            self.current_intensity_band = intensity_band

        else:
            print('no audio input fetched')

    def record(self):
        with sd.InputStream(device=self.device, channels=1, callback=self.callback,
                            blocksize=self.block_size,
                            samplerate=self.samplerate):
            while True:
                response = input()

    def hook_audio(self):
        print("hooking")
        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(self.record)
        print("hooked")
