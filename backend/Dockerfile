FROM python:3.11-slim

WORKDIR /app

# Set PYTHONPATH so Python can find modules inside /app/src
ENV PYTHONPATH=/app/src

COPY . .

RUN pip install --upgrade pip

# Install all requirements.txt files
RUN find . -name "requirements.txt" -exec pip install -r {} \;

# Set up environment if needed
RUN python src/setup/setup_env.py

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
