# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install production dependencies.
COPY Pipfile Pipfile.lock .
RUN pip install pipenv==2023.10.24
RUN pipenv install

# Code changes more frequently than dependencies, so we should copy our code
# only after dependencies are installed, to preserve layers in the cache.
COPY app.py main.py .
COPY assets ./assets
COPY my_project ./my_project

EXPOSE 8080

CMD pipenv run python main.py