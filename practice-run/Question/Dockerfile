FROM python:3.12-slim

WORKDIR /app

# git installed so the Q3 "set up Git in the Docker Compose" step can run in this service.
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Install deps first so the pip layer is cached.
COPY web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY web/ .

# Run as a non-root user (best practice; keeps SonarQube quieter later).
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
