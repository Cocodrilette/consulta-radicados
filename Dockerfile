FROM python:3.11-alpine

# Set environment variables
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
ENV HOME=/home/app
WORKDIR $HOME

# Install system dependencies
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
    musl-dev \
    linux-headers \
    && rm -rf /var/cache/apk/*

# Create non-root user for security
RUN addgroup -g 1000 app && \
    adduser -D -s /bin/bash -u 1000 -G app app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Change ownership to app user
RUN chown -R app:app $HOME

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000