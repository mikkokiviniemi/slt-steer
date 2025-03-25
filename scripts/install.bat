@echo off
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install pytest fastapi uvicorn google-generativeai langchain_google_genai langchain_community langchain_text_splitters pypdf chromadb google-cloud-storage langchain-chroma PyPDF2 python-dotenv
:: Install MongoDB-Related Dependencies
pip install motor pymongo
python src\setup_env.py
cd ../frontend
npm install
cd ..