from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MonedaDto(BaseModel):
    """DTO para representar una moneda."""
    id: int
    codigo: str  # Ej: USD, EUR, CLP
    nombre: str  # Ej: Dolar Estadounidense, Euro, Peso Chileno
    simbolo: str  # Ej: $, u20ac, $
    esta_activo: bool = True
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MonedaSummaryDto(BaseModel):
    """DTO para representar un resumen de moneda (para listados)."""
    id: int
    codigo: str
    simbolo: str
    
    class Config:
        from_attributes = True


class CrearMonedaCommand(BaseModel):
    """DTO para crear una nueva moneda."""
    codigo: str = Field(..., min_length=1, max_length=10)
    nombre: str = Field(..., min_length=1, max_length=100)
    simbolo: str = Field(..., min_length=1, max_length=5)


class ActualizarMonedaCommand(BaseModel):
    """DTO para actualizar una moneda existente."""
    id: int
    codigo: Optional[str] = Field(None, min_length=1, max_length=10)
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    simbolo: Optional[str] = Field(None, min_length=1, max_length=5)
    esta_activo: Optional[bool] = None
