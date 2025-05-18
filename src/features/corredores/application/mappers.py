"""
Mappers para transformar entidades de dominio en DTOs y viceversa.
"""
from ..domain.entities import Corredor as CorredorDomain
from .dtos import CorredorDto


def map_corredor_to_dto(corredor: CorredorDomain, id: int = None) -> CorredorDto:
    """
    Transforma una entidad de dominio Corredor en un DTO CorredorDto.
    
    Args:
        corredor: Entidad de dominio Corredor
        id: ID técnico del corredor (opcional, se obtiene de la capa de infraestructura)
        
    Returns:
        CorredorDto: DTO con la información del corredor
    """
    return CorredorDto(
        id=id,  # El ID se pasa desde la capa de infraestructura
        numero=corredor.numero,
        nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
        direccion=corredor.direccion,
        telefono=corredor.telefonos,
        email=corredor.mail,
        contacto=None,
        comision_default=0.0,
        esta_activo=corredor.fecha_baja is None
    )
