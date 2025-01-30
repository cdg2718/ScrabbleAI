# Use the official Python slim image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY main.py .
COPY xgboost_v0.json .
COPY requirements.txt .

# Update system packages and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    libomp-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 8080

# Define the command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]

