FROM python:3.11-slim

LABEL maintainer="AWS Bedrock App Generator"
LABEL description="Portable AWS Bedrock Application Generator"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
COPY adaptive_app_gen/ adaptive_app_gen/
COPY cli.py .
COPY README.md .
COPY QUICKSTART.py .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Create output directory
RUN mkdir -p generated_apps

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV OUTPUT_DIR=/app/generated_apps

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from adaptive_app_gen.bedrock_client import BedrockClient; BedrockClient()" || exit 1

# Default command
ENTRYPOINT ["python", "cli.py"]
CMD ["--help"]
