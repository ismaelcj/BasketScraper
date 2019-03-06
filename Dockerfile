FROM python:3.7

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app

RUN apt update
RUN apt install sqlite3

RUN pip install -r basketscraper/requirements.txt

# CMD ["python", "scripts/manage.py", "migrate"]
run python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
