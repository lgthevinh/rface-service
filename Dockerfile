# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Reinstall dlib after adding system dependencies
RUN pip install dlib

# Set environment variables
ENV DEEPFACE_HOME=/app/data/.deepface

# Copy DeepFace weights
COPY data/.deepface/weights /app/data/.deepface/weights

# Expose the Flask app's port
EXPOSE 2248

# Command to run the application
CMD ["python", "app/main.py"]
