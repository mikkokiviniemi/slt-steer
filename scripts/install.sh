#!/bin/bash

cd backend
python3 -m venv venv
source venv/bin/activate
find . -name "requirements.txt" | while read req; do
    echo "Installing dependencies from $req..."
    pip install -r "$req"
done
python src/setup/setup_env.py
cd ../frontend
npm install
cd ..
