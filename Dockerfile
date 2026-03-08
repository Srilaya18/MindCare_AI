# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirement list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
