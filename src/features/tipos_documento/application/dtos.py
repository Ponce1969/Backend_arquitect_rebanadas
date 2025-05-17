from typing import Optional

from pydantic import BaseModel, Field


class TipoDocumentoDto(BaseModel):
    """DTO para representar un tipo de documento."""
    id: int
    codigo: str  # Codigo unico (ej: DNI, RUT)
    nombre: str  # Nombre completo
    descripcion: Optional[str] = None  # Descripcion adicional
    es_default: bool = False  # Indica si es el tipo por defecto
    esta_activo: bool = True  # Indica si esta activo
    
    class Config:
        from_attributes = True


class TipoDocumentoSummaryDto(BaseModel):
    """DTO para representar un resumen de tipo de documento (para listados)."""
    id: int
    codigo: str
    nombre: str
    
    class Config:
        from_attributes = True


class CrearTipoDocumentoCommand(BaseModel):
    """DTO para crear un nuevo tipo de documento."""
    codigo: str = Field(..., min_length=1, max_length=10, description="Codigo unico del tipo de documento")
    nombre: str = Field(..., min_length=1, max_length=50, description="Nombre del tipo de documento")
    descripcion: Optional[str] = Field(None, max_length=200, description="Descripcion adicional")
    es_default: bool = Field(False, description="Indica si es el tipo por defecto")
    esta_activo: bool = Field(True, description="Indica si esta activo")


class ActualizarTipoDocumentoCommand(BaseModel):
    """DTO para actualizar un tipo de documento existente."""
    codigo: Optional[str] = Field(None, min_length=1, max_length=10)
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=200)
    es_default: Optional[bool] = None
    esta_activo: Optional[bool] = None
