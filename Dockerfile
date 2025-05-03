# Dockerfile
FROM python:3.11-slim

# Install dependencies
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY backend /app/backend
COPY .env /app/.env

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the Flask app
CMD ["python", "backend/app.py"]
