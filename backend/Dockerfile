FROM python:3.9-slim

WORKDIR /app

COPY ./src/. .
COPY ./tests .

RUN echo '#!/bin/bash\npython3 setup/setup_env.py\nuvicorn main:app --host 0.0.0.0 --port 8000' > start.sh \
    && chmod +x start.sh

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r ./ai_model/requirements.txt
RUN pip install --no-cache-dir -r ./database/requirements.txt
RUN pip install --no-cache-dir -r ./routes/requirements.txt
RUN pip install --no-cache-dir -r ./setup/requirements.txt

ENTRYPOINT ["./start.sh"]