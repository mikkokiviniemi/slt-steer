@echo off
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install fastapi uvicorn google-generativeai
cd ../frontend
npm install
cd ..