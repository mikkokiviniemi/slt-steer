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
        print("")


if __name__ == "__main__":
    setup_api_key()