import pvporcupine
import pyaudio
import struct
from .config import PORCUPINE_ACCESS_KEY, KPATH

def create_porcupine_instance():
    return pvporcupine.create(
        access_key=PORCUPINE_ACCESS_KEY,
        keyword_paths=KPATH
    )

def create_audio_stream(porcupine):
    pa = pyaudio.PyAudio()
    return pa, pa.open(
        format=pyaudio.paInt16,
        rate=porcupine.sample_rate,
        channels=1,
        input=True,
        output=True,
        frames_per_buffer=porcupine.frame_length
    )
