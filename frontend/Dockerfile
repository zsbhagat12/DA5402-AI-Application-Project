# frontend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend app
COPY . .

# Expose frontend Flask port
EXPOSE 8080

# Run the frontend Flask app
CMD ["python", "app.py"]
