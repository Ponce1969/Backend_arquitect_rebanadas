
from pydantic import field_validator, model_validator
from src.features.shared.validators.common import validate_codigo, validate_nombre, validate_simbolo


class MonedaValidators:
    """Clase con validadores para la entidad Moneda."""
    
    @classmethod
    @field_validator('codigo')
    def validate_codigo(cls, value: str) -> str:
        """Valida que el cu00f3digo de moneda tenga el formato correcto."""
        # Validación básica
        value = validate_codigo(value)
        
        # Validación específica para monedas (3 caracteres, como ISO 4217)
        if len(value) != 3:
            raise ValueError("El código de moneda debe tener exactamente 3 caracteres (formato ISO 4217)")
            
        return value
    
    @classmethod
    @field_validator('nombre')
    def validate_nombre(cls, value: str) -> str:
        """Valida que el    nombre de moneda tenga el formato correcto."""
        return validate_nombre(value, "nombre de moneda")
    
    @classmethod
    @field_validator('simbolo')
    def validate_simbolo(cls, value: str) -> str:
        """Valida que el símbolo de moneda tenga el formato correcto."""
        return validate_simbolo(value, "símbolo de moneda")
    
    @classmethod
    @model_validator(mode='after')
    def validate_moneda(cls, model):
        """Validaciones a nivel de modelo para la moneda."""
        # Ejemplo: validar que si el código es USD, el símbolo debe ser $
        if hasattr(model, 'codigo') and hasattr(model, 'simbolo'):
            if model.codigo == 'USD' and model.simbolo != '$':
                raise ValueError("El símbolo para USD debe ser $")
            elif model.codigo == 'EUR' and model.simbolo != '€':
                raise ValueError("El símbolo para EUR debe ser €")
        
        return model
