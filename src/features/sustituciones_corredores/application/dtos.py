from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


class SustitucionCorredorBase(BaseModel):
    """Modelo base para sustituciones de corredores."""
    corredor_ausente_numero: int = Field(..., gt=0, description="Número del corredor ausente")
    corredor_sustituto_numero: int = Field(..., gt=0, description="Número del corredor sustituto")
    fecha_inicio: date = Field(..., description="Fecha de inicio de la sustitución")
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin de la sustitución (opcional)")
    estado: str = Field("activa", description="Estado de la sustitución (activa/inactiva)")
    motivo: str = Field(..., min_length=2, max_length=200, description="Motivo de la sustitución")
    observaciones: Optional[str] = Field(None, max_length=500, description="Observaciones adicionales")
    
    @field_validator('fecha_fin')
    def fecha_fin_posterior_a_inicio(cls, v, info):
        if v and 'fecha_inicio' in info.data and v < info.data['fecha_inicio']:
            raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v
    
    @field_validator('corredor_sustituto_numero')
    def sustituto_diferente_de_ausente(cls, v, info):
        if 'corredor_ausente_numero' in info.data and v == info.data['corredor_ausente_numero']:
            raise ValueError('El corredor sustituto debe ser diferente al corredor ausente')
        return v
    
    model_config = ConfigDict(from_attributes=True)


class SustitucionCorredorCreate(SustitucionCorredorBase):
    """DTO para crear una sustitución de corredor."""
    pass


class SustitucionCorredorUpdate(BaseModel):
    """DTO para actualizar una sustitución de corredor."""
    corredor_sustituto_numero: Optional[int] = Field(None, gt=0, description="Número del corredor sustituto")
    fecha_inicio: Optional[date] = Field(None, description="Fecha de inicio de la sustitución")
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin de la sustitución")
    estado: Optional[str] = Field(None, description="Estado de la sustitución (activa/inactiva)")
    motivo: Optional[str] = Field(None, min_length=2, max_length=200, description="Motivo de la sustitución")
    observaciones: Optional[str] = Field(None, max_length=500, description="Observaciones adicionales")
    
    @field_validator('fecha_fin')
    def fecha_fin_valida(cls, v, info):
        if v and 'fecha_inicio' in info.data and info.data['fecha_inicio'] and v < info.data['fecha_inicio']:
            raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v
    
    model_config = ConfigDict(from_attributes=True)


class SustitucionCorredorInDB(SustitucionCorredorBase):
    """DTO para sustitución de corredor almacenada en la base de datos."""
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime


class SustitucionCorredorResponse(SustitucionCorredorBase):
    """DTO para respuesta de sustitución de corredor."""
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None


class FinalizarSustitucionRequest(BaseModel):
    """DTO para finalizar una sustitución de corredor."""
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin de la sustitución (por defecto, fecha actual)")
    observaciones: Optional[str] = Field(None, max_length=500, description="Observaciones adicionales sobre la finalización")
