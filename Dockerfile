# Use stable Debian base (NOT slim, NOT trixie)
FROM python:3.9-bullseye

# Set working directory
WORKDIR /app

# Environment configs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies REQUIRED for NLP
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model explicitly
RUN python -m spacy download en_core_web_sm

# Copy project files
COPY . .

# Railway exposes PORT dynamically
EXPOSE 8080

# Production server
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "app:app"]
