FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create dirs
RUN mkdir -p /app/data /app/tunnels

# Expose port
EXPOSE 4444

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:4444/ || exit 1

# Run (DATA_DIR so volume mount works)
ENV DATA_DIR=/app/data
CMD ["python", "c2.py"]