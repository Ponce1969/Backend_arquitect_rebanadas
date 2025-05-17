import re
from typing import Any, Callable, Optional

from pydantic import field_validator, Field, model_validator, ValidationInfo
from pydantic_core import PydanticCustomError


def validate_codigo(value: str, field_name: str = "codigo") -> str:
    """Valida que el código tenga el formato correcto (alfanumérico, mayúsculas)."""
    if not value:
        raise ValueError(f"El {field_name} no puede estar vacío")
        
    # Convertir a mayúsculas
    value = value.upper()
    
    # Validar que solo contenga caracteres alfanuméricos
    if not re.match(r'^[A-Z0-9]+$', value):
        raise ValueError(f"El {field_name} solo puede contener letras mayúsculas y números")
        
    return value


def validate_nombre(value: str, field_name: str = "nombre") -> str:
    """Valida que el nombre tenga el formato correcto."""
    if not value:
        raise ValueError(f"El {field_name} no puede estar vacío")
        
    # Eliminar espacios en blanco al inicio y al final
    value = value.strip()
    
    # Validar longitud mínima
    if len(value) < 2:
        raise ValueError(f"El {field_name} debe tener al menos 2 caracteres")
        
    return value


def validate_simbolo(value: str, field_name: str = "simbolo") -> str:
    """Valida que el símbolo tenga el formato correcto."""
    if not value:
        raise ValueError(f"El {field_name} no puede estar vacío")
        
    # Eliminar espacios en blanco al inicio y al final
    value = value.strip()
    
    # Validar longitud máxima
    if len(value) > 5:
        raise ValueError(f"El {field_name} no puede tener más de 5 caracteres")
        
    return value


def create_field_validator(field_name: str, validator_func: Callable) -> Callable:
    """Crea un validador de campo para Pydantic."""
    
    def validator(value: Any) -> Any:
        return validator_func(value, field_name)
    
    return validator
