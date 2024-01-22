# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . ./

# Install production dependencies.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD python main.py