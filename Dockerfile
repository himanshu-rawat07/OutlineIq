# Use a slim Python base image for small size (supports AMD64)
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy all local files to the container
COPY . .

# Install required Python library
RUN pip install --no-cache-dir PyMuPDF

# Entry point (runs when container starts)
CMD ["python", "main.py"]
