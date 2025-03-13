@echo off
cd frontend\src\tests
echo 🖼️✨ Running Vitest...
npx vitest --run
echo 🖼️✨ Vitest completed!
cd ..\..\..\
cd backend
echo ⚙️📦 Running pytest...
call venv\Scripts\activate
pytest -v tests/example_test.py
echo ⚙️📦 Pytest completed!