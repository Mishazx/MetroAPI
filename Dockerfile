FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP=run.py

CMD ["gunicorn", "-w", "2", "MetroAPI:app", "-b", "0.0.0.0:5000"]

