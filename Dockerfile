# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED=True

RUN apt-get update \
    && apt-get install --no-install-recommends -y gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /usr/local/bin/uv

# Use the image's Python 3.11 and keep the environment inside /app
ENV UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy the dependency files first so this layer is cached
COPY pyproject.toml uv.lock ./

# Install the locked production dependencies
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]
