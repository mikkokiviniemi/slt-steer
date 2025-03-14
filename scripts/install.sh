#!/bin/bash

cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
cd ../frontend
npm install
# Install vue-i18n for language support
npm install vue-i18n@9
cd ..
