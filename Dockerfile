# ===============================
# Customer Churn Prediction
# MLflow + DVC Dockerfile
# ===============================

FROM python:3.11-slim

# -------------------------------
# Environment variables

########## PYTHONDONTWRITEBYTECODE=1  ##########

# - Stops creation of __pycache__/ and .pyc
# - Keeps container clean

########## PYTHONUNBUFFERED=1  ##########

# - Logs are printed immediately
# - Critical for: Docker logs, MLflow logs, CI/CD pipelines
# - Without it → logs appear late or not at all

########## PIP_NO_CACHE_DIR=1  ##########

# - Prevents pip from caching wheels
# - Reduces image size
# - Without it → image bloats

# -------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# -------------------------------
# Set working directory
# -------------------------------
WORKDIR /app

# -------------------------------
# System dependencies

#### apt-get update ==> Updates Linux package index
#### build-essential ==> Includes: gcc, g++, make ==> Required for: numpy, sklearn 
###                  ==> Without it → pip install fails.

### rm -rf /var/lib/apt/lists/* ==> Deletes apt cache ==> Shrinks image size ==> Without it → +100MB image

# -------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Copy dependency files first

######## Why this order is CRITICAL ########

### ==> Docker caches layers.
### ==> If code changes → dependencies NOT reinstalled
### ==> If the code copied first → slow rebuilds every time
### ==> Therefore we copy dependency files first to leverage Docker layer caching.
# -------------------------------
COPY src/ src/
COPY requirements.txt .
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .

# -------------------------------
# Install Python dependencies
# -------------------------------
RUN pip install --upgrade pip \
    && pip install -r requirements.txt 

# -------------------------------
# Copy source code
# -------------------------------
COPY params.yaml .
COPY dvc.yaml .
COPY dvc.lock .
COPY . .

# -------------------------------
# Install project as a package
# (VERY IMPORTANT for -m usage)
# -------------------------------
RUN pip install -e .

# -------------------------------
# Create required directories
# -------------------------------
RUN mkdir -p artifacts mlruns

# -------------------------------
# Expose the ports
# -------------------------------
EXPOSE 8080

# -------------------------------
# Default command: Run full DVC pipeline
# -------------------------------
CMD ["python3", "app.py"]
