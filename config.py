import os
from dotenv import load_dotenv
import platform

load_dotenv()

# Configuration for API keys and environment-specific settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")

# Determine the OS
OPERATING_SYSTEM = platform.system()

# Path to the wake word model depending on the OS
KEYWORD_PATHS = {
    "Windows": ['windows/Hey-Stanley_en_windows_v3_0_0(1)/Hey-Stanley_en_windows_v3_0_0.ppn'],
    "Darwin": ['mac/Hey-Stanley_en_mac_v3_0_0/Hey-Stanley_en_mac_v3_0_0.ppn'],
    "Linux": ['placeholder for raspOs ppn/Unix']
}

KPATH = KEYWORD_PATHS.get(OPERATING_SYSTEM, ['default_path.ppn'])
