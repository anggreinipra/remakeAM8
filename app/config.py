import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = "db"  # Sesuai dengan nama service 'db' di docker-compose.yml
    
    # Koneksi PostgreSQL dengan menggunakan nama host db dan port 5432
    DB_URI = f"postgresql://postgres:postgres@{DB_HOST}:5432/revobank"
    
    # Menggunakan environment variable DATABASE_URL jika ada, jika tidak memakai DB_URI
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", DB_URI)
    
    # Menonaktifkan SQLALCHEMY_TRACK_MODIFICATIONS untuk efisiensi
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Menentukan JWT secret key, gunakan value dari .env atau default key
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")

class TestConfig(Config):
    # Menggunakan SQLite untuk testing, tanpa koneksi ke PostgreSQL
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    
    # Mengaktifkan mode testing
    TESTING = True
