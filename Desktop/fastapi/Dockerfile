# Dockerfile for the Celery Worker service

# 1. Base image - updated to Python 3.11 to match local environment
FROM python:3.11-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Create a non-root user for Celery
RUN groupadd -r celery && useradd -r -g celery celery

# 4. Set the working directory in the container
WORKDIR /usr/src/app

# 5. Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code
COPY . .

# 7. Change ownership of the app directory to celery user
RUN chown -R celery:celery /usr/src/app

# 8. Switch to non-root user
USER celery

# 9. Default command to run the Celery worker
CMD ["celery", "-A", "worker.celery_app", "worker", "-I", "tasks", "--loglevel=info"]