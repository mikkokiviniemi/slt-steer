@echo off
cd backend
call venv\Scripts\activate
pytest -v tests/example_test.py
