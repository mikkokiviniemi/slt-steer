#!/bin/bash

cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
cd ../frontend
npm install
cd ..
