@echo off
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install fastapi uvicorn google-generativeai langchain_google_genai langchain_community langchain_text_splitters pypdf chromadb google-cloud-storage langchain-chroma PyPDF2
cd ../frontend
npm install
cd ..