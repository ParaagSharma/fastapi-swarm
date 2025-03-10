FROM python:3.12

RUN apt-get update && apt-get install -y postgresql-client netcat-openbsd

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8011

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload", "--port", "8011"]
