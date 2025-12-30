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

# Make the run script executable
RUN chmod +x /app/run.sh

# Expose the port your app runs on
ENV PORT=8080
EXPOSE $PORT

# Define the command to start your application
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn eccgd_backend.wsgi:application --bind 0.0.0.0:8080"]