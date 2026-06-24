# Base image (starting image)
# Docker needs a base image to build a new image
# This image contains Linux + Python 3.11 + pip
FROM python:3.11-slim

# Set the working directory inside the container
# All following commands will run from /app
WORKDIR /app

# Copy requirements.txt from local machine to /app in the container
COPY requirements.txt .

# Install all Python dependencies listed in requirements.txt
# --no-cache-dir reduces image size by not storing pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project folder into the container
COPY . .

# Inform Docker that the application listens on port 5001
# Note: This does not publish the port to the host machine
EXPOSE 5001

# Default command executed when the container starts
# Equivalent to running: python app.py
CMD ["python", "app.py"]