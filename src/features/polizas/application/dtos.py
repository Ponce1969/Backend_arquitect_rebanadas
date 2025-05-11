from datetime import date
from typing import Optional, List
import uuid

from pydantic import BaseModel, Field, validator

# Importamos el Enum TipoDuracion del dominio
from src.features.polizas.domain.types import TipoDuracion

# Importamos DTOs relacionados (asumimos que existen)
from src.features.clientes.application.dtos import ClienteDto
from src.features.corredores.application.dtos import CorredorDto
from src.features.tipos_seguros.application.dtos import TipoSeguroDto
# from src.domain.shared.dtos import MonedaDto  # Asumimos que existe


# DTO para crear una nueva pu00f3liza (entrada a EmitirPolizaUseCase)
class EmitirPolizaCommand(BaseModel):
    cliente_id: uuid.UUID
    corredor_id: Optional[int] = None
    tipo_seguro_id: int
    carpeta: Optional[str] = None
    numero_poliza: str
    endoso: Optional[str] = None
    fecha_inicio: date
    fecha_vencimiento: date
    fecha_emision: Optional[date] = None
    estado_poliza: str = "activa"
    forma_pago: Optional[str] = None
    tipo_endoso: Optional[str] = None
    moneda_id: Optional[int] = None
    suma_asegurada: float
    prima: float
    comision: Optional[float] = None
    cuotas: Optional[int] = None
    observaciones: Optional[str] = None
    tipo_duracion: TipoDuracion = TipoDuracion.anual
    
    # Validadores
    @validator("fecha_vencimiento")
    def fecha_vencimiento_posterior_a_inicio(cls, v, values):
        if "fecha_inicio" in values and v <= values["fecha_inicio"]:
            raise ValueError("La fecha de vencimiento debe ser posterior a la fecha de inicio")
        return v
    
    @validator("comision")
    def comision_positiva(cls, v):
        if v is not None and v < 0:
            raise ValueError("La comisiu00f3n no puede ser negativa")
        return v


# DTO para actualizar una pu00f3liza existente (entrada a ActualizarPolizaUseCase)
class ActualizarPolizaCommand(BaseModel):
    id: int  # ID de la pu00f3liza a actualizar
    corredor_id: Optional[int] = None
    carpeta: Optional[str] = None
    endoso: Optional[str] = None
    fecha_vencimiento: Optional[date] = None
    fecha_emision: Optional[date] = None
    estado_poliza: Optional[str] = None
    forma_pago: Optional[str] = None
    tipo_endoso: Optional[str] = None
    moneda_id: Optional[int] = None
    suma_asegurada: Optional[float] = None
    prima: Optional[float] = None
    comision: Optional[float] = None
    cuotas: Optional[int] = None
    observaciones: Optional[str] = None
    tipo_duracion: Optional[TipoDuracion] = None
    
    # Validadores
    @validator("comision")
    def comision_positiva(cls, v):
        if v is not None and v < 0:
            raise ValueError("La comisiu00f3n no puede ser negativa")
        return v


# DTO para representar una Pu00f3liza (salida de Use Cases y API)
class PolizaDto(BaseModel):
    id: int
    cliente: ClienteDto  # DTO completo del cliente
    corredor: Optional[CorredorDto] = None  # DTO completo del corredor
    tipo_seguro: TipoSeguroDto  # DTO completo del tipo de seguro
    carpeta: Optional[str] = None
    numero_poliza: str
    endoso: Optional[str] = None
    fecha_inicio: date
    fecha_vencimiento: date
    fecha_emision: Optional[date] = None
    estado_poliza: str
    forma_pago: Optional[str] = None
    tipo_endoso: Optional[str] = None
    # moneda: Optional[MonedaDto] = None  # DTO completo de la moneda
    suma_asegurada: float
    prima: float
    comision: Optional[float] = None
    cuotas: Optional[int] = None
    observaciones: Optional[str] = None
    tipo_duracion: TipoDuracion
    
    # Propiedades calculadas
    @property
    def is_active(self) -> bool:
        today = date.today()
        return self.fecha_inicio <= today <= self.fecha_vencimiento and self.estado_poliza == "activa"
    
    @property
    def comision_monto(self) -> Optional[float]:
        if self.comision is not None and self.prima is not None:
            return (self.prima * self.comision) / 100.0
        return None
    
    class Config:
        from_attributes = True  # Para mapear desde objetos SQLAlchemy
        json_encoders = {
            date: lambda v: v.isoformat(),
            uuid.UUID: lambda v: str(v)
        }


# DTO para representar un resumen de Pu00f3liza (para listados)
class PolizaSummaryDto(BaseModel):
    id: int
    cliente_id: uuid.UUID
    cliente_nombre: str  # Solo el nombre del cliente, no el objeto completo
    corredor_numero: Optional[int] = None
    corredor_nombre: Optional[str] = None  # Solo el nombre del corredor, no el objeto completo
    tipo_seguro_nombre: str  # Solo el nombre del tipo de seguro, no el objeto completo
    numero_poliza: str
    fecha_inicio: date
    fecha_vencimiento: date
    estado_poliza: str
    suma_asegurada: float
    prima: float
    
    # Propiedades calculadas
    @property
    def is_active(self) -> bool:
        today = date.today()
        return self.fecha_inicio <= today <= self.fecha_vencimiento and self.estado_poliza == "activa"
    
    class Config:
        from_attributes = True  # Para mapear desde objetos SQLAlchemy
        json_encoders = {
            date: lambda v: v.isoformat(),
            uuid.UUID: lambda v: str(v)
        }