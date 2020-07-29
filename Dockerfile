FROM python:3.6-slim

RUN pip install pipenv
WORKDIR /app
ADD . /app
RUN chmod +x /app/app.py
RUN pipenv install --ignore-pipfile --deploy --system