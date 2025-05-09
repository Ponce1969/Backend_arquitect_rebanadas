from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, HttpUrl, validator


class AseguradoraBase(BaseModel):
    """Modelo base para aseguradoras."""
    nombre: str = Field(..., min_length=1, max_length=100)
    identificador_fiscal: Optional[str] = Field(None, max_length=12)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    pagina_web: Optional[str] = Field(None, max_length=100)
    esta_activa: bool = True
    observaciones: Optional[str] = None

    class Config:
        orm_mode = True


class AseguradoraCreate(AseguradoraBase):
    """DTO para crear una aseguradora."""
    pass


class AseguradoraUpdate(BaseModel):
    """DTO para actualizar una aseguradora."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    identificador_fiscal: Optional[str] = Field(None, max_length=12)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    pagina_web: Optional[str] = Field(None, max_length=100)
    esta_activa: Optional[bool] = None
    observaciones: Optional[str] = None

    class Config:
        orm_mode = True


class AseguradoraInDB(AseguradoraBase):
    """DTO para aseguradora almacenada en la base de datos."""
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime


class AseguradoraResponse(AseguradoraInDB):
    """DTO para respuesta de aseguradora."""
    pass
