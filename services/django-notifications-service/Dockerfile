FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["sh", "-c", \
    "python manage.py migrate --noinput && \
     python manage.py loaddata fixtures/notifications.json --ignorenonexistent && \
     gunicorn notifications_config.wsgi:application --bind 0.0.0.0:8002 --workers 2"]