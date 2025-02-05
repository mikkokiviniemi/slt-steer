@echo off
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install fastapi uvicorn
cd ../frontend
npm install
cd ..