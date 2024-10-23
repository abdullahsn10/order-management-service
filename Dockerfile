# Stage 1: Build Stage
FROM python:3.10-alpine AS builder

# Set the working directory for the build stage
WORKDIR /app

# Install build dependencies (essential for compiling)
RUN apk update && apk add --no-cache\
    postgresql-dev\
    gcc\
    musl-dev\
    libffi-dev\
    build-base

# Copy the requirements file into the build stage
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code into the build stage
COPY . .

# Stage 2: Runtime Stage
FROM python:3.10-alpine

# Set the working directory for the runtime stage
WORKDIR /app

# Install only the necessary runtime dependencies
RUN apk update && apk add --no-cache \
    libpq \
    bash

# Copy the installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app /app

# Expose the ports the app runs on and the gRPC port
EXPOSE 8888 50051

# Define the command to run the application
CMD ["python", "server.py"]
