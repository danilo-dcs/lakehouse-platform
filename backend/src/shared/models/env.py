from pydantic_settings import BaseSettings

class EnvSettings(BaseSettings):
    BACKEND_ENV: str = None
    EMAIL_SERVICE_KEY: str = None
    PASSPORT_BROKER_SERVICE_URL: str = None
    COUCHBASE_HOST: str = None
    COUCHBASE_USER: str = None
    COUCHBASE_PASSWORD: str = None
    COUCHBASE_BUCKET: str = None
    ENCRYPTION_SECRET_KET: str = None
    AUTH_SECRET_KEY: str = None        
    REFRESH_TOKEN_KEY: str = None      
    AUTH_ALGORITHM: str = None
    EXPIRATION_TIME_MINUTES: int = None
    FRONTEND_URL: str = None
    DOCUMENTATION_URL: str = None
    BACKEND_DOMAIN_URL: str = None
    COUCHBASE_DOMAIN_URL: str = None

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'allow'  # Allows extra environment variables