# Use an official Python runtime as a parent image
FROM python:3.11.7-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    iputils-ping \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container at /app
COPY Rag/requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy only the contents of the Rag directory into the container at /app
COPY Rag /app

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run the FastAPI server using the specified command
CMD ["python3", "./api.py"]
