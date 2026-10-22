# Use a lightweight base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency mappings
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source configuration
COPY app.py .

# Expose production engine network port
EXPOSE 5000

# Define runtime launch script
CMD ["python", "app.py"]
