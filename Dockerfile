FROM python:3.10.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app


# Install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# Create necessary directories
RUN mkdir -p /app/staticfiles
RUN mkdir -p /app/media

# Copy requirements first
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY src/backend/ .

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Make entrypoint script executable
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
