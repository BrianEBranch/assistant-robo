import openai
from openai import OpenAI
import speech_recognition as sr
import pvporcupine
import pyaudio
import struct
import platform
import time
from gtts import gTTS
from playsound import playsound
import os

# get necessary keys from system env variables.
openai.api_key =
porcupine_access_key =

# create recognizer object and microphone object from speech_recognition library.
recognizer = sr.Recognizer()
mic = sr.Microphone()

#get os name, in order to determine which functions are to be used since some are platform dependent.
opSystem = platform.system()

#create gpt assistant object
client = OpenAI()
stanley = client.beta.assistants.create(
    instructions="You are Stanley, a helpful assistant tasked with helping the user in any safe way possible. RESPOND "
                 "AS CONCISE AS POSSIBLE.",
    name="Stanley",
    description="Stanley is a jarvis like AI-Assistant meant to help the user with day to day task.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini",
    temperature=0.3,
)
# get_gpt3_response takes in a some prompt and generates a response using the appropriate parameters.
# then returns the first element in choices since gpt responses are arrays and strips the whitespace from the response.
def get_gpt3_response(prompt):
    print("fix")
    #currently needs ot be updated since openai no longer supports completions


# speak is a function that takes in some text and writes that text to our mp3 file which gets converted to tts
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("responses/response.mp3")
    playsound("responses/response.mp3")

if(opSystem=="Windows"):
    kPath = ['windows/Hey-Stanley_en_windows_v3_0_0(1)/Hey-Stanley_en_windows_v3_0_0.ppn']
elif(opSystem=="Darwin"):
    kPath = ['mac/Hey-Stanley_en_mac_v3_0_0/Hey-Stanley_en_mac_v3_0_0.ppn']
else:
    kPath = ['placeholder for raspOs ppn/Unix']

porcupine = pvporcupine.create(
    access_key=porcupine_access_key,
    keyword_paths=kPath
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
                audio = recognizer.listen(source,10,5)
                print(audio)
                print("here")
                try:
                    print("try here")
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
