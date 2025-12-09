from celery import Celery
import os

# Get REDIS_HOST from environment, default to localhost for host machine
# This allows FastAPI (on host) to use localhost, and Celery worker (in Docker) to use redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

celery_app = Celery(
    "worker",
    broker=f"redis://{REDIS_HOST}:6379/0",
    backend=f"redis://{REDIS_HOST}:6379/0"
)