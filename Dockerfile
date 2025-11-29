FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/logs

# Copy the rest of the application's code
COPY . .
COPY eccgd-lms-backend-credentials.json /app/eccgd-lms-backend-credentials.json

# Make the run script executable
RUN chmod +x /app/run.sh

# Set GCP credentials environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/eccgd-lms-backend-credentials.json

EXPOSE 8000

# The main command to run when the container starts
# This will run the migrations and then start the Gunicorn server
CMD ["/app/run.sh"]
