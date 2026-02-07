FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir requests

COPY test_nginx.py .

CMD ["python", "test_nginx.py"]
