from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CorredorBase(BaseModel):
    """Modelo base para corredores."""
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del corredor")
    documento: str | None = Field(None, min_length=6, max_length=20, description="Documento de identidad")
    direccion: str = Field(..., min_length=2, max_length=200, description="Dirección completa")
    localidad: str | None = Field(None, max_length=100, description="Localidad o ciudad")
    telefono: str = Field(..., min_length=6, max_length=20, description="Teléfono fijo")
    movil: str | None = Field(None, min_length=6, max_length=20, description="Teléfono móvil")
    email: EmailStr = Field(..., description="Correo electrónico")
    contacto: str | None = Field(None, max_length=100, description="Persona de contacto")
    observaciones: str | None = Field(None, description="Observaciones adicionales")
    matricula: str | None = Field(None, max_length=50, description="Número de matrícula")
    especializacion: str | None = Field(None, max_length=100, description="Área de especialización")
    comision_default: float = Field(0.0, ge=0.0, le=100.0, description="Porcentaje de comisión por defecto (0-100)")
    
    class Config:
        from_attributes = True


class CorredorCreate(CorredorBase):
    """DTO para crear un corredor."""
    pass


class CorredorUpdate(BaseModel):
    """DTO para actualizar un corredor."""
    nombre: str | None = Field(None, min_length=2, max_length=100, description="Nombre completo del corredor")
    documento: str | None = Field(None, min_length=6, max_length=20, description="Documento de identidad")
    direccion: str | None = Field(None, min_length=2, max_length=200, description="Dirección completa")
    localidad: str | None = Field(None, max_length=100, description="Localidad o ciudad")
    telefono: str | None = Field(None, min_length=6, max_length=20, description="Teléfono fijo")
    movil: str | None = Field(None, min_length=6, max_length=20, description="Teléfono móvil")
    email: EmailStr | None = Field(None, description="Correo electrónico")
    contacto: str | None = Field(None, max_length=100, description="Persona de contacto")
    observaciones: str | None = Field(None, description="Observaciones adicionales")
    matricula: str | None = Field(None, max_length=50, description="Número de matrícula")
    especializacion: str | None = Field(None, max_length=100, description="Área de especialización")
    comision_default: float | None = Field(None, ge=0.0, le=100.0, description="Porcentaje de comisión por defecto (0-100)")
    esta_activo: bool | None = Field(None, description="Indica si el corredor está activo")
    
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