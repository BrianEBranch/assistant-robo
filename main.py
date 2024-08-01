from openai import OpenAI
from gtts import gTTS
from playsound import playsound
from dotenv import load_dotenv
from datetime import datetime
import speech_recognition as sr
import platform
import struct
import openai
import pvporcupine
import pyaudio
import os
import run
import re
import fRecognition

# get necessary keys from system env variables.
load_dotenv()
openai.api_key = "OPENAI_API_KEY"
porcupine_access_key = "PORCUPINE_ACCESS_KEY"

# create recognizer object and microphone object from speech_recognition library.
recognizer = sr.Recognizer()
mic = sr.Microphone()

# get os name, in order to determine which functions are to be used since some are platform dependent.
opSystem = platform.system()
# create gpt assistant object
client = OpenAI()
# create thread, basically a conversation between user and ai.
# if thread is created up here, stanley will retain memory of previous conversations.
thread = client.beta.threads.create()
#TODO instead of creating a new assistant I will pull one from openai api.
stanley = client.beta.assistants.create(
    instructions="You are Stanley, a helpful assistant tasked with helping the user in any safe way possible. RESPOND "
                 "AS CONCISE AS POSSIBLE.",
    name="Stanley",
    description="Stanley is a jarvis like AI-Assistant meant to help the user with day to day task.",
    model="gpt-4o-mini",
)

def getPath():
    if (opSystem == "Windows"):
        kPath = ['windows/Hey-Stanley_en_windows_v3_0_0(1)/Hey-Stanley_en_windows_v3_0_0.ppn']
    elif (opSystem == "Darwin"):
        kPath = ['mac/Hey-Stanley_en_mac_v3_0_0/Hey-Stanley_en_mac_v3_0_0.ppn']
    else:
        kPath = ['placeholder for raspOs ppn/Unix']
    return kPath


porcupine = pvporcupine.create(
    access_key=porcupine_access_key,
    keyword_paths=getPath()
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
# speak is a function that takes in some text and writes that text to our mp3 file which gets converted to tts
def speak(text):
    tts = gTTS(text=text, lang='en')
    if (text == "Hello, I am at your service"):
        playsound("responses/stanley_hello.mp3")
    elif (text == "I couldn't understand"):
        playsound("responses/stanley_error.mp3")
    else:
        formattedTime = datetime.now().strftime("%D:%M:%Y:%S")
        fileName = f"responses_on_{formattedTime}.mp3"
        # remove characters that are invalid for filenames
        fileName = re.sub(r'[<>:"/\\|?*]', '', fileName)
        tts.save(f"responses/{fileName}")
        playsound(f"responses/{fileName}")


# get_gpt3_response takes in a some prompt and generates a response using the appropriate parameters.
# then returns the first element in choices since gpt responses are arrays and strips the whitespace from the response.
def get_gpt3_response(text):
    # on each iteration create a new message from user request
    event_handler = run.EventHandler()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text
    )
    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=stanley.id,
            instructions="You are Stanley, a helpful assistant tasked with helping the user in any safe way possible."
                         "RESPOND AS CONCISE AS POSSIBLE.",
            event_handler=event_handler,
    ) as stream:
        stream.until_done()
        speak(event_handler.generated_text)


try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack('h' * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)
        print(keyword_index)
        #TODO doesn't work need to somehow have the program continually watch for people until wakeword then return people in frame
        names = fRecognition.recognize_face(keyword_index)
        if keyword_index >= 0:
            print("entered name checking")
            greetings = ""
            for name in names:
                greetings += name + ", "
            print(greetings)
            speak(f"Hello, {greetings}")
            with sr.Microphone() as source:
                audio = recognizer.listen(source, None, 5)
                try:
                    text = recognizer.recognize_google(audio)
                    get_gpt3_response(text)
                except sr.UnknownValueError:
                    speak("I couldn't understand")
                except sr.RequestError as e:
                    speak("Could not request results from Google Cloud service; {0}".format(e))
finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
