@echo off
cd backend
call venv\Scripts\activate
cd src
start uvicorn main:app --reload
