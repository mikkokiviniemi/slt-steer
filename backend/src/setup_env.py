import os
from dotenv import load_dotenv, set_key
from logging_config import logger, log_event

dotenv_path = '.env'

def setup_api_key():
    load_dotenv(dotenv_path)
    if not os.getenv('GEMINI_API'):
        api_key = input("Enter Gemini API-key: ")
        set_key(dotenv_path, 'GEMINI_API', api_key)
        log_event("200 OK", "Gemini API-key saved.")
    else:
        log_event("200 OK", "Gemini API-key already defined.")

def setup_google_credential_path():
    load_dotenv(dotenv_path)
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        google_credential_path = input("Enter GOOGLE_APPLICATION_CREDENTIALS path: ")
        set_key(dotenv_path, 'GOOGLE_APPLICATION_CREDENTIALS', google_credential_path)
        log_event("200 OK", "GOOGLE_APPLICATION_CREDENTIALS saved.")
    else:
        log_event("200 OK", "GOOGLE_APPLICATION_CREDENTIALS already defined.")

if __name__ == "__main__":
    setup_api_key()
    setup_google_credential_path()
