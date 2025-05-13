import os
from typing import Any

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación."""
    
    # Configuración de la API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "API Seguros"
    
    # Configuración de seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "insecure_key_for_dev")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días
    
    # Configuración de la base de datos
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "api_seguros")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None
    
    # Configuración de email
    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None
    
    # Credenciales de administrador inicial
    FIRST_SUPERUSER_NAME: str = "admin"
    FIRST_SUPERUSER_LASTNAME: str = "admin"
    FIRST_SUPERUSER_EMAIL: str = "admin@apiseguros.com"
    FIRST_SUPERUSER_USERNAME: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"
    
    # Configuración del frontend
    FRONTEND_URL: str = "http://localhost:5173"
    
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info) -> Any:
        if isinstance(v, str):
            return v
            
        # En Pydantic v2, accedemos a los datos a través del objeto ValidationInfo
        data = info.data
        user = data.get("POSTGRES_USER")
        password = data.get("POSTGRES_PASSWORD")
        host = data.get("POSTGRES_SERVER")
        port = data.get("POSTGRES_PORT")
        db = data.get("POSTGRES_DB", "")
        
        # Construir manualmente la URL de conexión
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"
    
    # Configuración de CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default
    ]
    
    # Configuración de email
    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"  # Permitir campos adicionales en Pydantic v2


# Instancia global de configuración
settings = Settings()
