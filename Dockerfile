# Use official Python 3.11 slim image to avoid Python 3.14 wheel issues
FROM python:3.11-slim

# Install system dependencies required by some Python packages (Pillow, lxml, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libxml2-dev \
    libxslt1-dev \
    wget \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the app
COPY . /app

# Expose Streamlit default port
ENV PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false

# Start Streamlit
CMD ["streamlit", "run", "main.py", "--server.port", "${PORT}", "--server.address", "0.0.0.0"]
