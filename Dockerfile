# Use a specific Python version for consistency
FROM python:3.9-slim

# Install system dependencies required for building certain Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files into the container
COPY . /app/

# Copy the models directory into the container
COPY models/ /app/models/

# Expose the necessary port (if required by your app)
EXPOSE 5000

# Command to run your application
CMD ["python", "wsgi.py"]
