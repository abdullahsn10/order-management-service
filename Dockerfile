# Stage 1: Build Stage
FROM python:3.10-alpine AS builder

WORKDIR /app

RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    libffi-dev \
    build-base

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Runtime Stage
FROM python:3.10-alpine

WORKDIR /app

RUN apk update && apk add --no-cache \
    libpq \
    bash

# Copy the installed Python packages from the builder stage, and entrypoint commands
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

EXPOSE 8888 50051

CMD ["python", "server.py"]
