# Gunakan base image python
FROM python:3.11-slim

# Set environment variable agar Python tidak meng-cache .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy semua source code ke dalam container
COPY . .

# Jalankan aplikasi dengan uv (bukan uvicorn)
CMD ["uv", "icorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
