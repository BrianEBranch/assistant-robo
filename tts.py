from gtts import gTTS
from playsound import playsound
from datetime import datetime
import re
import os

RESPONSES_DIR = "responses"

def speak(text):
    if text == "Hello, I am at your service":
        playsound(os.path.join(RESPONSES_DIR, "stanley_hello.mp3"))
    elif text == "I couldn't understand":
        playsound(os.path.join(RESPONSES_DIR, "stanley_error.mp3"))
    else:
        formatted_time = datetime.now().strftime("%I:%M:%S %p")
        file_name = re.sub(r'[<>:"/\\|?*]', '', f"responses_on_{formatted_time}.mp3")
        file_path = os.path.join(RESPONSES_DIR, file_name)
        tts = gTTS(text=text, lang='en')
        tts.save(file_path)
        playsound(file_path)
