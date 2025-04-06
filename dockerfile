# Gunakan base image python
FROM python:3.11-slim

# Set environment variable agar Python tidak meng-cache .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy source code
COPY . .

# Run app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
ENV FLASK_APP=main.py


