#!/bin/bash

cd backend
python3 -m venv venv
source venv/bin/activate
pip install pytest fastapi uvicorn google-generativeai langchain_google_genai langchain_community langchain_text_splitters pypdf chromadb google-cloud-storage langchain-chroma PyPDF2 python-dotenv
python src/setup_env.py
cd ../frontend
npm install
# Install vue-i18n for language support
npm install vue-i18n@9
cd ..
