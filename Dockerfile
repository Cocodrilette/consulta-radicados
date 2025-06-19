# Use Python Alpine
FROM python:3.13.5-alpine

# Set working directory
ENV HOME=/home/app
WORKDIR $HOME

# Copy project files
COPY . .

RUN apk add --no-cache \
    chromium \
    chromium-chromedriver


# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
