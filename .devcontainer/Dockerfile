# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install Docker, nodejs, npm, and netcat-openbsd
RUN apt-get update && \
    apt-get install -y \
    nodejs \
    npm \
    netcat-openbsd \
    curl \
    gnupg \
    lsb-release && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Ganache CLI
RUN npm install -g ganache-cli

# Install Truffle
RUN npm install -g truffle

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set the entry point to bash to allow for manual control
ENTRYPOINT ["/bin/bash"]