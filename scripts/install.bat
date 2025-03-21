@echo off
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install pytest fastapi uvicorn google-generativeai langchain_google_genai langchain_community langchain_text_splitters pypdf chromadb google-cloud-storage langchain-chroma PyPDF2 python-dotenv motor pymongo
python src\setup_env.py
for /f "delims=" %%i in ('dir /b /s requirements.txt 2^>nul') do (
    echo Installing dependencies from %%i...
    pip install -r "%%i"
)
python src\setup\setup_env.py
cd ../frontend
npm install
cd ..