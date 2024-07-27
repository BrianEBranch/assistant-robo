import openai
import speech_recognition as sr
import pvporcupine
import pyaudio
import struct
import time
from gtts import gTTS
import os

# get necessary keys from system env variables.
openai.api_key = os.getenv("OPENAI_API_KEY")
porcupine_access_key = os.getenv("PORCUPINE_ACCESS_KEY")

# create recognizer object and microphone object from speech_recognition library.
recognizer = sr.Recognizer()
mic = sr.Microphone()


# get_gpt3_response takes in a some prompt and generates a response using the appropriate parameters.
# then returns the first element in choices since gpt responses are arrays and strips the whitespace from the response.
def get_gpt3_response(prompt):
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=150,
    )
    return response.choices[0].text.strip()


# speak is a function that takes in some text and writes that text to our mp3 file which gets converted to tts
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("responses/response.mp3")
    os.system("afplay responses/response.mp3")


porcupine = pvporcupine.create(
    access_key=porcupine_access_key,
    keyword_paths=['Hey-Stanley_en_mac_v3_0_0/Hey-Stanley_en_mac_v3_0_0.ppn']
)

pa = pyaudio.PyAudio()
audio_stream = pa.open(
    format=pyaudio.paInt16,
    rate=porcupine.sample_rate,
    channels=1,
    input=True,
    output=True,
    frames_per_buffer=porcupine.frame_length
)


try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack('h' * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            with sr.Microphone() as source:
                speak("Hello, I am at your service")
                audio = recognizer.listen(source)
                try:
                    text = recognizer.recognize_google(audio)
                    response = get_gpt3_response(text)
                    speak(response)
                except sr.UnknownValueError:
                    speak("I couldn't understand")
                except sr.RequestError as e:
                    speak("Could not request results from Google Cloud service; {0}".format(e))
finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
