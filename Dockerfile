#  Python runtime
FROM python:3.11-alpine

# Working directory
WORKDIR /app

# Check requirements
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy content into the container
COPY . .

# Expose a port
EXPOSE 5000

# Entrypoint
CMD ["python", "demo.py"]
