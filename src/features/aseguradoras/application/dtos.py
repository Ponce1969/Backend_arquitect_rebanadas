from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class AseguradoraBase(BaseModel):
    """Modelo base para aseguradoras."""
    nombre: str = Field(..., min_length=1, max_length=100)
    identificador_fiscal: str | None = Field(None, max_length=12)
    telefono: str | None = Field(None, max_length=20)
    direccion: str | None = Field(None, max_length=200)
    email: EmailStr | None = None
    pagina_web: str | None = Field(None, max_length=100)
    esta_activa: bool = True
    observaciones: str | None = None

    class Config:
        from_attributes = True


class AseguradoraCreate(AseguradoraBase):
    """DTO para crear una aseguradora."""
    pass


class AseguradoraUpdate(BaseModel):
    """DTO para actualizar una aseguradora."""
    nombre: str | None = Field(None, min_length=1, max_length=100)
    identificador_fiscal: str | None = Field(None, max_length=12)
    telefono: str | None = Field(None, max_length=20)
    direccion: str | None = Field(None, max_length=200)
    email: EmailStr | None = None
    pagina_web: str | None = Field(None, max_length=100)
    esta_activa: bool | None = None
    observaciones: str | None = None

    class Config:
        from_attributes = True


class AseguradoraInDB(AseguradoraBase):
    """DTO para aseguradora almacenada en la base de datos."""
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime


class AseguradoraResponse(AseguradoraInDB):
    """DTO para respuesta de aseguradora."""
    pass


# Alias para compatibilidad con otros slices
AseguradoraDto = AseguradoraResponse
