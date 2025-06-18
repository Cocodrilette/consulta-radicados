# Use Python Alpine
FROM python:3.11-alpine

# Set working directory
ENV HOME=/home/app
WORKDIR $HOME

# Copy project files
COPY . .

# Install necessary packages
RUN apk add --no-cache \
    bash \
    chromium \
    chromium-chromedriver \
    curl \
    unzip \
    freetype \
    ttf-dejavu \
    font-noto \
    font-noto-cjk \
    font-noto-emoji \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver
