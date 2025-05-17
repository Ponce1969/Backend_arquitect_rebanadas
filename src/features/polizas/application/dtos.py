from datetime import date
from typing import Optional, List
import uuid

from pydantic import BaseModel, Field, field_validator

# Importamos el Enum TipoDuracion del dominio
from src.features.polizas.domain.types import TipoDuracion

# Importamos DTOs relacionados
from src.features.clientes.application.dtos import ClienteDto
from src.features.corredores.application.dtos import CorredorDto
from src.features.tipos_seguros.application.dtos import TipoSeguroDto
from src.domain.shared.dtos import MonedaDto


# DTO para crear una nueva poliza (entrada a EmitirPolizaUseCase)
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
    @field_validator("fecha_vencimiento")
    @classmethod
    def fecha_vencimiento_posterior_a_inicio(cls, v, values):
        if "fecha_inicio" in values and v <= values["fecha_inicio"]:
            raise ValueError("La fecha de vencimiento debe ser posterior a la fecha de inicio")
        return v
    
    @field_validator("comision")
    @classmethod
    def comision_positiva(cls, v):
        if v is not None and v < 0:
            raise ValueError("La comisión no puede ser negativa")
        return v
    
    @field_validator("moneda_id")
    @classmethod
    def validate_moneda_required_for_international(cls, v, values):
        # Si la suma asegurada es alta o hay indicios de póliza internacional, la moneda es obligatoria
        if "suma_asegurada" in values and values["suma_asegurada"] > 100000 and v is None:
            raise ValueError("Para pólizas con sumas aseguradas altas, la moneda es obligatoria")
        return v


# DTO para actualizar una poliza existente (entrada a ActualizarPolizaUseCase)
class ActualizarPolizaCommand(BaseModel):
    id: int  # ID de la poliza a actualizar
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
    @field_validator("comision")
    @classmethod
    def comision_positiva(cls, v):
        if v is not None and v < 0:
            raise ValueError("La comisión no puede ser negativa")
        return v


# DTO para representar una poliza (salida de Use Cases y API)
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
    moneda: Optional[MonedaDto] = None  # DTO completo de la moneda
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


# DTO para representar un resumen de poliza (para listados)
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
    moneda_codigo: Optional[str] = None  # Solo el código de la moneda, no el objeto completo
    moneda_simbolo: Optional[str] = None  # Solo el símbolo de la moneda
    
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
