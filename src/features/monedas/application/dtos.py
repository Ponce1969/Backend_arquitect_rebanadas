from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, field_validator, model_validator, ValidationInfo
from src.features.monedas.application.validators.moneda_validators import MonedaValidators
from src.domain.shared.exceptions import ValidationError


class MonedaDto(BaseModel):
    """DTO para representar una moneda."""
    id: int
    codigo: str  # Ej: USD, EUR, CLP
    nombre: str  # Ej: Dolar Estadounidense, Euro, Peso Chileno
    simbolo: str  # Ej: $, €, $
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
    codigo: str = Field(..., description="Cu00f3digo ISO de la moneda (3 caracteres)")
    nombre: str = Field(..., description="Nombre completo de la moneda")
    simbolo: str = Field(..., description="Su00edmbolo utilizado para representar la moneda")
    
    # Validadores de campo
    validate_codigo = field_validator('codigo')(MonedaValidators.validate_codigo)
    validate_nombre = field_validator('nombre')(MonedaValidators.validate_nombre)
    validate_simbolo = field_validator('simbolo')(MonedaValidators.validate_simbolo)
    
    # Validador de modelo - usamos el decorador directamente para evitar problemas de firma
    @model_validator(mode='after')
    def validate_model(cls, model):
        return MonedaValidators.validate_moneda(model)
    
    @classmethod
    def validate_and_create(cls, data: Dict[str, Any]) -> 'CrearMonedaCommand':
        """Valida los datos y crea una instancia del comando."""
        try:
            return cls(**data)
        except ValueError as e:
            # Convertir errores de validaciu00f3n de Pydantic a nuestras excepciones personalizadas
            raise ValidationError(details={"errors": str(e)})


class ActualizarMonedaCommand(BaseModel):
    """DTO para actualizar una moneda existente."""
    id: int = Field(..., description="ID de la moneda a actualizar")
    codigo: Optional[str] = Field(None, description="Cu00f3digo ISO de la moneda (3 caracteres)")
    nombre: Optional[str] = Field(None, description="Nombre completo de la moneda")
    simbolo: Optional[str] = Field(None, description="Su00edmbolo utilizado para representar la moneda")
    esta_activo: Optional[bool] = Field(None, description="Indica si la moneda estu00e1 activa")
    
    # Validadores condicionales (solo se aplican si el campo no es None)
    @field_validator('codigo')
    def validate_codigo(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            return MonedaValidators.validate_codigo(value)
        return value
    
    @field_validator('nombre')
    def validate_nombre(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            return MonedaValidators.validate_nombre(value)
        return value
    
    @field_validator('simbolo')
    def validate_simbolo(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            return MonedaValidators.validate_simbolo(value)
        return value
    
    # Validador de modelo
    @model_validator(mode='after')
    def validate_model(cls, model):
        # Verificar que al menos un campo de actualizaciu00f3n estu00e1 presente
        update_fields = [
            model.codigo is not None,
            model.nombre is not None,
            model.simbolo is not None,
            model.esta_activo is not None
        ]
        
        if not any(update_fields):
            raise ValueError("Debe proporcionar al menos un campo para actualizar")
        
        # Aplicar validaciones adicionales solo si los campos relevantes estu00e1n presentes
        if model.codigo is not None and model.simbolo is not None:
            # Llamar al validador de moneda con el formato correcto
            MonedaValidators.validate_moneda(model)
            
        return model
    
    @classmethod
    def validate_and_create(cls, data: Dict[str, Any]) -> 'ActualizarMonedaCommand':
        """Valida los datos y crea una instancia del comando."""
        try:
            return cls(**data)
        except ValueError as e:
            # Convertir errores de validaciu00f3n de Pydantic a nuestras excepciones personalizadas
            raise ValidationError(details={"errors": str(e)})
