"""
gemini_chat.py

Tämä moduuli tarjoaa GeminiChat-luokan, jonka avulla voi käydä keskusteluja
Google gemini -kielimallin kanssa.

Example: 
folder_name = "data"
os.makedirs(folder_name, exist_ok=True)
data = gemini_chat.download_pdfs_from_bucket("training_data-1","data/data.txt")
gemini_chat_system = gemini_chat.GeminiChat(api_key=google_api_key,temperature=0, max_output_tokens=2000, model="gemini-2.0-flash-lite", document_content=data)
"""

import io
import os
import PyPDF2
from google import genai
from google.genai import types
from google.cloud import storage

def download_pdfs_from_bucket(bucket_name,local_path) -> str:
    if os.path.exists(local_path):
        with open(local_path, "r") as file:
            content = file.read()
        print("File exists. Using existing data\n")

        return content
    else:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs()

        all_text = ""

        for blob in blobs:
            if blob.name.lower().endswith(".pdf"):
                print(f"Downloading {blob.name} from {bucket_name}...")
                all_text += blob.name + "\n"
                try:
                    pdf_content = blob.download_as_bytes()
                    pdf_file = io.BytesIO(pdf_content)
                    reader = PyPDF2.PdfReader(pdf_file)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            all_text += text + "\n"
                except PyPDF2.errors.PdfReadError as e:
                    return f"Error reading PDF file {blob.name}: {e}"
                except Exception as e:
                    return f"Error processing PDF file {blob.name}: {e}"

        if not all_text:
            return "No PDF files found or no text extracted from PDFs."
        
        with open(local_path, "w") as file:
            file.write(all_text)

        return all_text


class GeminiChat:
    def __init__(self, api_key, temperature=0, max_output_tokens=500, model="gemini-2.0-flash-lite", document_content=""):

        self.client = genai.Client(api_key=api_key)
        self.system_instruction = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context and chat history to answer the question. "
            "Do not use any outside knowledge or make assumptions. "
            "Use three sentences maximum for the main answer and keep the response concise. "

            "If the question is in English and the information is found in the context, first provide a concise answer. "
            "Then, naturally continue the conversation by asking a relevant follow-up question based on the user's query and chat history. "

            "If the question is in Finnish and the information is found in the context, first provide a concise answer. "
            "Sen jälkeen jatka keskustelua luontevasti kysymällä aiheeseen liittyvän jatkokysymyksen, joka auttaa käyttäjää syventämään ymmärrystään ottaen huomioon aikaisemman keskustelun. "

            "If the question is in English and the information is not found in the context, say: "
            "'Unfortunately, I do not have enough information on the topic you asked about. I recommend reaching out to a specialist or your healthcare provider if needed.' "
            "Then, naturally ask a relevant follow-up question based on the chat history to better understand the user's concern. "

            "If the question is in Finnish and the information is not found in the context, say: "
            "'Valitettavasti minulla ei ole riittävästi tietoa esittämääsi aiheeseen. Suosittelen ottamaan yhteyttä asiantuntijaan tai hoitavaan tahoon tarvittaessa.' "
            "Tämän jälkeen kysy luontevasti jatkokysymys, joka auttaa käyttäjää tarkentamaan tilannettaan ottaen huomioon aikaisemman keskustelun. "
            "\n\n"
            "Context: {document_content}"
        )

        self.chat = self.client.chats.create(
                        model=model,
                        config=types.GenerateContentConfig(
                            system_instruction=self.system_instruction,
                            temperature = temperature,
                            max_output_tokens = max_output_tokens
                        ),
                    )

    def generate_response(self, user_input: str) -> str:
        response = self.chat.send_message(user_input)
        return response.text