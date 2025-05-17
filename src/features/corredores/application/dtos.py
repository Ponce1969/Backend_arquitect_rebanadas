from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CorredorBase(BaseModel):
    """Modelo base para corredores."""
    nombre: str = Field(..., min_length=2, max_length=100)
    direccion: str = Field(..., min_length=2, max_length=200)
    telefono: str = Field(..., min_length=6, max_length=20)
    email: EmailStr
    contacto: str | None = Field(None, max_length=100)
    comision_default: float = Field(0.0, ge=0.0, le=100.0)  # Porcentaje entre 0 y 100
    esta_activo: bool = True
    
    class Config:
        from_attributes = True


class CorredorCreate(CorredorBase):
    """DTO para crear un corredor."""
    pass


class CorredorUpdate(BaseModel):
    """DTO para actualizar un corredor."""
    nombre: str | None = Field(None, min_length=2, max_length=100)
    direccion: str | None = Field(None, min_length=2, max_length=200)
    telefono: str | None = Field(None, min_length=6, max_length=20)
    email: EmailStr | None = None
    contacto: str | None = Field(None, max_length=100)
    comision_default: float | None = Field(None, ge=0.0, le=100.0)
    esta_activo: bool | None = None
    
    class Config:
        from_attributes = True


class CorredorInDB(CorredorBase):
    """DTO para corredor almacenado en la base de datos."""
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime


class CorredorDto(CorredorInDB):
    """DTO para respuesta de corredor."""
    pass


class CorredorSearchParams(BaseModel):
    """Parámetros para búsqueda de corredores."""
    query: str | None = None
    esta_activo: bool | None = None