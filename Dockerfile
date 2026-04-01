# Simplified Dockerfile - no Playwright needed
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install system dependencies for WeasyPrint and MediaPipe
# Install system dependencies for OpenCV/MediaPipe
RUN apt-get update && apt-get install -y --no-install-recommends \
    # OpenCV/MediaPipe dependencies
    libgl1 \
    libglib2.0-0 \
    # Utilities
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Copy font files for text overlay rendering
COPY fonts/ /app/fonts/

# Copy and set executable permissions for entrypoint script
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port (only used by web service)
EXPOSE 8000

# Health check (only used by web service)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1

# Entrypoint script decides whether to run web server or worker
# Set SERVICE_TYPE environment variable: "web" or "worker"
ENTRYPOINT ["/app/docker-entrypoint.sh"]
