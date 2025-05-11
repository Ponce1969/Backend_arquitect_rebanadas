from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class ClienteBase(BaseModel):
    """Modelo base para clientes."""
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    tipo_documento_id: int
    numero_documento: str = Field(..., min_length=1, max_length=50)
    fecha_nacimiento: date
    direccion: str = Field(..., min_length=1, max_length=200)
    localidad: str | None = Field(None, max_length=50)
    telefonos: str = Field(..., min_length=1, max_length=100)
    movil: str = Field(..., min_length=1, max_length=100)
    mail: EmailStr
    observaciones: str | None = None

    class Config:
        orm_mode = True


class ClienteCreate(ClienteBase):
    """DTO para crear un cliente."""
    creado_por_id: int
    modificado_por_id: int


class ClienteUpdate(BaseModel):
    """DTO para actualizar un cliente."""
    nombres: str | None = Field(None, min_length=1, max_length=100)
    apellidos: str | None = Field(None, min_length=1, max_length=100)
    tipo_documento_id: int | None = None
    numero_documento: str | None = Field(None, min_length=1, max_length=50)
    fecha_nacimiento: date | None = None
    direccion: str | None = Field(None, min_length=1, max_length=200)
    localidad: str | None = Field(None, max_length=50)
    telefonos: str | None = Field(None, min_length=1, max_length=100)
    movil: str | None = Field(None, min_length=1, max_length=100)
    mail: EmailStr | None = None
    observaciones: str | None = None
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


# Alias para compatibilidad con otros slices
ClienteDto = ClienteResponse


class ClienteSearchParams(BaseModel):
    """Parámetros para búsqueda de clientes."""
    query: str | None = None
    tipo_documento_id: int | None = None
    localidad: str | None = None
