from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class BaseDto(BaseModel):
    """Clase base para todos los DTOs del sistema."""
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class AuditableDto(BaseDto):
    """Clase base para DTOs que incluyen campos de auditoría."""
    fecha_creacion: Optional[datetime] = Field(
        None, 
        description="Fecha de creación del registro"
    )
    fecha_actualizacion: Optional[datetime] = Field(
        None, 
        description="Fecha de la última actualización del registro"
    )

# Utilidades de validación
def validar_telefono(telefono: str) -> str:
    """Valida que el número de teléfono tenga un formato válido."""
    if not telefono:
        return telefono
    
    # Eliminar cualquier carácter que no sea dígito
    solo_numeros = ''.join(c for c in telefono if c.isdigit())
    
    # Validar longitud mínima y máxima
    if not (8 <= len(solo_numeros) <= 15):
        raise ValueError("El teléfono debe tener entre 8 y 15 dígitos")
    
    return telefono.strip()

def validar_porcentaje(porcentaje: float) -> float:
    """Valida que el porcentaje esté entre 0 y 100."""
    if not (0 <= porcentaje <= 100):
        raise ValueError("El porcentaje debe estar entre 0 y 100")
    return porcentaje

def validar_contrasena_segura(contrasena: str) -> str:
    """Valida que la contraseña cumpla con los requisitos de seguridad."""
    if len(contrasena) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    if not any(c.isupper() for c in contrasena):
        raise ValueError("La contraseña debe contener al menos una letra mayúscula")
    if not any(c.islower() for c in contrasena):
        raise ValueError("La contraseña debe contener al menos una letra minúscula")
    if not any(c.isdigit() for c in contrasena):
        raise ValueError("La contraseña debe contener al menos un número")
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in contrasena):
        raise ValueError("La contraseña debe contener al menos un carácter especial")
    return contrasena
