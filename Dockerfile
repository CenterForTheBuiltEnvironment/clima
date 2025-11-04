# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED=True

RUN apt-get update \
    && apt-get install --no-install-recommends -y gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir "pipenv>=2024.0,<2026.0"
# Set working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv sync

COPY . .

EXPOSE 8080

CMD ["pipenv", "run", "python", "main.py"]
