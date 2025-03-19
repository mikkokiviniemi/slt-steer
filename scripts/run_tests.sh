#!/bin/bash
cd frontend/src/tests
echo "🖼️✨ Running Vitest..."
npx vitest --run
echo "🖼️✨ Vitest completed!"
cd ../../../
cd backend
echo " "
source venv/bin/activate
echo "⚙️📦 Running pytest..."
pytest -v tests/example_test.py
echo "⚙️📦 Pytest completed!"