import keyring
import config

# pip install keyring, before running set api key script
# pip install keyring needs to be added to script!

print("Enter your Gemini API key:")
api_key = input()
keyring.set_password(config.SERVICE_NAME, config.USERNAME, api_key)
print("API key stored securely.")

# add to git, run before using app
