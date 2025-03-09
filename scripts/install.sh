#!/bin/bash

cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn google-generativeai langchain_google_genai langchain_community langchain_text_splitters pypdf chromadb google-cloud-storage langchain-chroma PyPDF2
cd ../frontend
npm install
cd ..