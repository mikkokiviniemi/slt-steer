"""
utils.py

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""

import re
import io
import os
import PyPDF2
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

# Yksinkertainen HTML-formatoija, jos haluat säilyttää samaa logiikkaa
def formatGeminiResponse(text: str) -> str:
    # Lihavoi **merkinnät**
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Muunna markdown-listat HTML-listoiksi
    lines = text.split("\n")
    for i, line in enumerate(lines):
        match = re.match(r'^\*\s+(.*?)$', line)
        if match:
            lines[i] = f"- {match.group(1)}"

    return "<br>".join(lines)
