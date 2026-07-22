FROM python:3.12-slim

WORKDIR /app

# git is installed so the Q3 "set up Git in the Docker Compose" step can run here.
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first so the pip layer is cached.
COPY web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY web/ .

# Run as a non-root user (SonarQube/Docker best practice).
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
