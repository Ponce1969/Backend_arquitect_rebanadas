from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class ClienteCorredorDto(BaseModel):
    """DTO para representar la relación entre un cliente y un corredor."""
    cliente_id: UUID
    corredor_numero: int
    fecha_asignacion: date
    
    class Config:
        from_attributes = True


class AsignarClienteCorredorCommand(BaseModel):
    """DTO para asignar un cliente a un corredor."""
    cliente_id: UUID = Field(..., description="ID del cliente a asignar")
    corredor_numero: int = Field(..., description="Número del corredor al que se asignará el cliente")
    fecha_asignacion: date | None = Field(None, description="Fecha de asignación (por defecto, la fecha actual)")


class ReasignarClienteCommand(BaseModel):
    """DTO para reasignar un cliente de un corredor a otro."""
    cliente_id: UUID = Field(..., description="ID del cliente a reasignar")
    corredor_numero_antiguo: int = Field(..., description="Número del corredor actual")
    corredor_numero_nuevo: int = Field(..., description="Número del nuevo corredor")
    fecha_asignacion: date | None = Field(None, description="Fecha de asignación (por defecto, la fecha actual)")
