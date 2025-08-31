import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///vulnscan.db'

    # Scanning configuration
    MAX_PORTS = 65535
    DEFAULT_TIMEOUT = 5
    MAX_THREADS = 100

    # Security settings
    BCRYPT_LOG_ROUNDS = 12
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
