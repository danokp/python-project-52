FROM python:3.10.0-alpine

ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 8000

CMD poetry run python manage.py migrate
CMD poetry run gunicorn -w 5 -b 0.0.0.0:8000 task_manager.wsgi
