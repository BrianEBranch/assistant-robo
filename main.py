import struct
import speech_recognition as sr
from tts import speak
from gpt import get_gpt3_response
from wake_word import create_porcupine_instance, create_audio_stream

recognizer = sr.Recognizer()


def main():
    porcupine = create_porcupine_instance()
    pa, audio_stream = create_audio_stream(porcupine)

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack('h' * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                speak("Hello, I am at your service")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, None, 6)
                    try:
                        text = recognizer.recognize_google(audio)
                        response = get_gpt3_response(text)
                        speak(response)
                    except sr.UnknownValueError:
                        speak("I couldn't understand")
                    except sr.RequestError as e:
                        speak(f"Could not request results from Google Cloud service; {0}".format(e))
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()


if __name__ == "__main__":
    main()
