import os
from dotenv import load_dotenv

dotenv_path = '.env'

def print_status(key):
    value = os.getenv(key)
    if value:
        print(f"\n{key} is already defined.\n")
    else:
        raise EnvironmentError(f"{key} is not set! Please provide it via environment or .env")

def setup_all():
    load_dotenv(dotenv_path)

    # Check for required keys
    print_status('GEMINI_API')
    print_status('GOOGLE_APPLICATION_CREDENTIALS')
    print_status('MONGO_URI')

if __name__ == "__main__":
    setup_all()
