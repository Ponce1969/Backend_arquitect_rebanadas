from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator

# Importamos el DTO de Aseguradora para incluirlo en nuestros DTOs
from src.features.aseguradoras.application.dtos import AseguradoraDto


# DTOs para entrada (Commands)
class CreateTipoSeguroCommand(BaseModel):
    """Comando para crear un nuevo tipo de seguro."""
    codigo: str = Field(..., min_length=1, max_length=10)
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None
    es_default: bool = False
    esta_activo: bool = True
    categoria: str = Field(..., min_length=2, max_length=30)
    cobertura: str = Field(...)
    vigencia_default: int = Field(1, ge=1)  # Mayor o igual a 1
    aseguradora_id: int = Field(...)
    
    @field_validator('codigo')
    @classmethod
    def codigo_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('El código no puede estar vacío')
        return v.upper()  # Convertir a mayúsculas
    
    class Config:
        json_schema_extra = {
            "example": {
                "codigo": "AUTO001",
                "nombre": "Seguro Automotriz Completo",
                "descripcion": "Cobertura completa para vehículos particulares",
                "es_default": True,
                "esta_activo": True,
                "categoria": "AUTOMOTRIZ",
                "cobertura": "Daños a terceros, robo, incendio y destrucción total",
                "vigencia_default": 12,
                "aseguradora_id": 1
            }
        }


class UpdateTipoSeguroCommand(BaseModel):
    """Comando para actualizar un tipo de seguro existente."""
    id: int = Field(...)
    codigo: str = Field(..., min_length=1, max_length=10)
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None
    es_default: bool = False
    esta_activo: bool = True
    categoria: str = Field(..., min_length=2, max_length=30)
    cobertura: str = Field(...)
    vigencia_default: int = Field(1, ge=1)  # Mayor o igual a 1
    aseguradora_id: int = Field(...)
    
    @field_validator('codigo')
    @classmethod
    def codigo_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('El código no puede estar vacío')
        return v.upper()  # Convertir a mayúsculas
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "codigo": "AUTO001",
                "nombre": "Seguro Automotriz Completo Actualizado",
                "descripcion": "Cobertura completa para vehículos particulares",
                "es_default": True,
                "esta_activo": True,
                "categoria": "AUTOMOTRIZ",
                "cobertura": "Daños a terceros, robo, incendio y destrucción total",
                "vigencia_default": 12,
                "aseguradora_id": 1
            }
        }


# DTOs para salida
class TipoSeguroDto(BaseModel):
    """DTO para representar un tipo de seguro completo."""
    id: int
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    es_default: bool
    esta_activo: bool
    categoria: str
    cobertura: str
    vigencia_default: int
    aseguradora: AseguradoraDto
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    # Propiedades calculadas
    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} ({self.codigo})"
    
    @property
    def vigencia_en_meses(self) -> int:
        return self.vigencia_default
    
    class Config:
        from_attributes = True


class TipoSeguroSummaryDto(BaseModel):
    """DTO para representar un resumen de tipo de seguro."""
    id: int
    codigo: str
    nombre: str
    categoria: str
    es_default: bool
    esta_activo: bool
    aseguradora_id: int
    aseguradora_nombre: str
    
    class Config:
        from_attributes = True
