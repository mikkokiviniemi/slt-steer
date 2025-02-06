import google.generativeai as genai
import os

genai.configure(api_key=os.environ['gemini-api'])

model = genai.GenerativeModel('gemini-1.5-flash-002')
response = model.generate_content('Anna esimerkki potilaan valmistautumisohjeista pallonlaajennusoperaatioon')

print(response.text)