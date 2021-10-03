# syntax=docker/dockerfile:1

FROM python:3.9.7-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app.py app.py

COPY backend/ backend/

COPY frontend/ frontend/

COPY README.md README.md

ARG DB

ENV DATABASE_URL $DB

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
