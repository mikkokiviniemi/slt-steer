import os
from dotenv import load_dotenv, set_key

dotenv_path = '.env'

def setup_api_key():
    load_dotenv(dotenv_path)
    if not os.getenv('GEMINI_API'):
        api_key = input("Enter Gemini API-key: ")
        set_key(dotenv_path, 'GEMINI_API', api_key)
        print("") # Empty prints for better readability
        print("Gemini API-key saved.")
        print("")
    else:
        print("") # Empyty prints for better readability
        print("Gemini API-key is already defined.")
        set_key(dotenv_path, 'GEMINI_API', os.getenv('GEMINI_API'))
        print("")

def setup_mongo_uri():
    load_dotenv(dotenv_path)
    if not os.getenv('MONGO_URI'):
        MONGO_URI = input("Enter MONGO_URI: ")
        set_key(dotenv_path, 'MONGO_URI', MONGO_URI)
        print("") # Empty prints for better readability
        print("MONGO_URI saved.")
        print("")
    else:
        print("") # Empyty prints for better readability
        print("MONGO_URI is already defined.")
        set_key(dotenv_path, 'MONGO_URI', os.getenv('MONGO_URI'))
        print("")


def setup_google_credential_path():
    load_dotenv(dotenv_path)
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        google_credential_path = input("Enter GOOGLE_APPLICATION_CREDENTIALS path: ")
        set_key(dotenv_path, 'GOOGLE_APPLICATION_CREDENTIALS', google_credential_path)
        print("") # Empty prints for better readability
        print("GOOGLE_APPLICATION_CREDENTIALS saved.")
        print("")
    else:
        print("") # Empyty prints for better readability
        print("GOOGLE_APPLICATION_CREDENTIALS is already defined.")
        set_key(dotenv_path, 'GOOGLE_APPLICATION_CREDENTIALS', os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        print("")


if __name__ == "__main__":
    setup_api_key()
    setup_google_credential_path()
    setup_mongo_uri()