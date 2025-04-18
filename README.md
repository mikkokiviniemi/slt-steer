![LOGO](https://github.com/mikkokiviniemi/slt-steer/blob/main/frontend/src/assets/logo.png)
# Heartwise (slt-steer) 
![workflow](https://github.com/mikkokiviniemi/slt-steer/actions/workflows/main.yml/badge.svg)
[![Last Commit](https://img.shields.io/github/last-commit/mikkokiviniemi/slt-steer)](https://github.com/mikkokiviniemi/slt-steer)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/mikkokiviniemi/slt-steer/blob/main/LICENSE)


## 💡 About
A web application (with mobile phone view) that provides individualized treatment guidance for (heart disease) patients.

## 🛠️ Installation and running 
### Installation and running on Windows
```bash
cd slt-steer
.\scripts\install.bat
```
```bash
.\scripts\run_backend.bat
```
```bash
.\scripts\run_frontend.bat
```
### Installation and running on Linux
```bash
cd slt-steer
./scripts/install.sh
```
```bash
./scripts/run_backend.sh
```
```bash
./scripts/run_frontend.sh
```
## 🧪 Testing
### Testing on Windows
```bash
.\scripts\run_tests.bat
```
### Testing on Linux
```bash
./scripts/run_tests.sh
```

## 🐳 Docker
This project supports Docker for running, testing, and development.
### 🧪 Tested With
This project has been tested with the following versions:
- **Docker**: 28.1.0 (build 4d8c241)
- **Docker Compose**: v2.35.0
Ensure you have compatible versions installed to avoid issues.
---

## 🔐 Environment Setup
To run the application and tests successfully, you must provide the required credentials and environment variables.
### 📁 Required Files and Locations
Ensure the following files exist in your project:
#### 1. Google Cloud credentials JSON
/slt-steer/cloud_storage_key.json
This file contains your Google Cloud service account key used for authentication.
#### 2. Backend environment file
/slt-steer/backend/.env
This file must contain the following environment variables:

```env
GEMINI_API=your_google_gemini_api_key
GOOGLE_APPLICATION_CREDENTIALS=/app/cloud_storage_key.json
MONGO_URI=your_mongo_connection_string
```

## 🧰 Tech Stack
### Frontend
*TODO*
### Backend
*TODO*
### AI model
*TODO*

## 📜 License
This project is licensed under the [MIT License](https://github.com/mikkokiviniemi/slt-steer/blob/main/LICENSE)

## 👥 Authors
- [elsingit](https://github.com/elsingit)
- [JoonasKarna](https://github.com/JoonasKarna)
- [kirsimarianne](https://github.com/kirsimarianne)
- [matiashaapasalmi](https://github.com/matiashaapasalmi)
- [mikkokiviniemi](https://github.com/mikkokiviniemi)
- [pasasalm](https://github.com/pasasalm)
- [riinaeer](https://github.com/riinaeer)

## Contribution
🚫 **Please do not contribute to this project.**  

This is a school project intended for educational purposes only. The repository is made public for sharing and demonstration, but we are not accepting contributions or pull requests. This is an group assignment for a course. The project scope is intentionally limited to course requirements.

Thank you for your understanding!
