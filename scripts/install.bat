@echo off
cd backend
python -m venv venv
call venv\Scripts\activate.bat
for /f "delims=" %%i in ('dir /b /s requirements.txt 2^>nul') do (
    echo Installing dependencies from %%i...
    pip install -r "%%i"
)
python src\setup\setup_env.py
cd ../frontend
npm install
cd ..