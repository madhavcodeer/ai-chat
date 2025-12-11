# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Node.js (required for building the frontend)
RUN apt-get update && apt-get install -y nodejs npm git

# Copy the current directory contents into the container at /app
COPY . /app

# 1. Build Frontend
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# 2. Setup Backend
WORKDIR /app
# Upgrade pip to avoid compilation issues
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Render will provide
EXPOSE 10000

# Run the smart start script
RUN chmod +x run_app.sh
CMD ["./run_app.sh"]
