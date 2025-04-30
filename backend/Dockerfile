# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose port used by Flask API
EXPOSE 5000

# Run the backend Flask app
CMD ["python", "server.py"]
