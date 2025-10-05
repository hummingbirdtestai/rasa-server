# -----------------------------
# Base image: Python 3.10
# -----------------------------
FROM python:3.10-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory inside container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Train model
RUN rasa train

# Expose Rasa port
EXPOSE 10000

# Start Rasa server with actions
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "10000", "--actions", "actions"]
