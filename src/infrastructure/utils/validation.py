from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel, ValidationError as PydanticValidationError

# Actualizada la importación a la ubicación correcta
from src.domain.shared.exceptions import ValidationError

T = TypeVar('T', bound=BaseModel)


def validate_model(model_class: Type[T], data: Union[Dict[str, Any], BaseModel]) -> T:
    """Valida datos contra un modelo Pydantic.
    
    Args:
        model_class: Clase del modelo Pydantic a utilizar para la validación.
        data: Datos a validar, puede ser un diccionario o un modelo Pydantic.
        
    Returns:
        Una instancia del modelo Pydantic con los datos validados.
        
    Raises:
        ValidationError: Si los datos no cumplen con las validaciones del modelo.
    """
    try:
        if isinstance(data, dict):
            return model_class(**data)
        elif isinstance(data, BaseModel):
            return model_class(**data.dict())
        else:
            raise ValidationError(
                "Los datos deben ser un diccionario o un modelo Pydantic"
            )
    except PydanticValidationError as e:
        errors = []
        for error in e.errors():
            field = error.get('loc', ['unknown'])[0]
            message = error.get('msg', 'Error de validación')
            errors.append(f"{field}: {message}")
        
        raise ValidationError(
            "Error de validación en los datos",
            details={"errors": errors}
        )


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """Valida que todos los campos requeridos estén presentes en los datos.
    
    Args:
        data: Diccionario con los datos a validar.
        required_fields: Lista de nombres de campos requeridos.
        
    Raises:
        ValidationError: Si alguno de los campos requeridos no está presente o es None.
    """
    missing_fields = []
    
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
    
    if missing_fields:
        raise ValidationError(
            f"Faltan campos requeridos: {', '.join(missing_fields)}",
            details={"errors": [f"{field}: Este campo es requerido" for field in missing_fields]}
        )
