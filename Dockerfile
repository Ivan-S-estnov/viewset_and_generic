FROM python:3.13

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./



COPY . .

ENV SECRET_KEY="your_secret_key"
ENV CELERY_BROKER_URL="your_celery_broker_url"
ENV CELERY_BACKEND="your_celery_backend"

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]