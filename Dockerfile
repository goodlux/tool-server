# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY config/ config/
COPY scripts/ scripts/

# Make script executable
RUN chmod +x scripts/download_toolsets.sh

# Download configured toolsets on container start
ENTRYPOINT ["./scripts/download_toolsets.sh"]
CMD ["python", "-m", "src.server"]
