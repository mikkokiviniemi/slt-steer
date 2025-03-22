@echo off
cd backend
python -m venv venv
call venv\Scripts\activate.bat
for /r %%i in (requirements.txt) do (
    echo Installing dependencies from %%i...
    pip install -r "%%i"
)
python src\setup\setup_env.py
cd ../frontend
npm install
cd ..