# Use a full Debian-based Python image
FROM python:3.10

# Install dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    netcat-openbsd \
    curl \
    gnupg \
    lsb-release \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Install Ganache CLI
RUN npm install -g ganache-cli

# Install Truffle
RUN npm install -g truffle

# Set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Expose port 5000
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set the entry point
ENTRYPOINT ["/bin/bash"]
