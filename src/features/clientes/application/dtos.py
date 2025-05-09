from datetime import date, datetime
from typing import Optional, UUID

from pydantic import BaseModel, Field, EmailStr, validator


class ClienteBase(BaseModel):
    """Modelo base para clientes."""
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    tipo_documento_id: int
    numero_documento: str = Field(..., min_length=1, max_length=50)
    fecha_nacimiento: date
    direccion: str = Field(..., min_length=1, max_length=200)
    localidad: Optional[str] = Field(None, max_length=50)
    telefonos: str = Field(..., min_length=1, max_length=100)
    movil: str = Field(..., min_length=1, max_length=100)
    mail: EmailStr
    observaciones: Optional[str] = None

    class Config:
        orm_mode = True


class ClienteCreate(ClienteBase):
    """DTO para crear un cliente."""
    creado_por_id: int
    modificado_por_id: int


class ClienteUpdate(BaseModel):
    """DTO para actualizar un cliente."""
    nombres: Optional[str] = Field(None, min_length=1, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo_documento_id: Optional[int] = None
    numero_documento: Optional[str] = Field(None, min_length=1, max_length=50)
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = Field(None, min_length=1, max_length=200)
    localidad: Optional[str] = Field(None, max_length=50)
    telefonos: Optional[str] = Field(None, min_length=1, max_length=100)
    movil: Optional[str] = Field(None, min_length=1, max_length=100)
    mail: Optional[EmailStr] = None
    observaciones: Optional[str] = None
    modificado_por_id: int

    class Config:
        orm_mode = True


class ClienteInDB(ClienteBase):
    """DTO para cliente almacenado en la base de datos."""
    id: UUID
    numero_cliente: int
    creado_por_id: int
    modificado_por_id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime


class ClienteResponse(ClienteInDB):
    """DTO para respuesta de cliente."""
    pass


class ClienteSearchParams(BaseModel):
    """Parámetros para búsqueda de clientes."""
    query: Optional[str] = None
    tipo_documento_id: Optional[int] = None
    localidad: Optional[str] = None
