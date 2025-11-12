FROM python:3.11-slim

WORKDIR /app

COPY . /app  
COPY requirements.txt .
#COPY .env ./.env

RUN pip install -r requirements.txt

ENV FLASK_APP=app

EXPOSE 5000

CMD ["flask", "--app", "weather_app.app", "run", "--host", "0.0.0.0", "--port", "5000"]