
from src.features.shared.mappers import Mapper, DTOMapper
from src.features.monedas.domain.entities import Moneda as MonedaEntity
from src.features.monedas.infrastructure.models import Moneda as MonedaModel
from src.features.monedas.application.dtos import (
    MonedaDto, 
    MonedaSummaryDto,
    CrearMonedaCommand
)


class MonedaMapper(Mapper):
    """Mapper entre la entidad Moneda y el modelo MonedaModel."""
    
    @staticmethod
    def to_entity(model: MonedaModel) -> MonedaEntity:
        """Convierte un modelo de Moneda a una entidad de dominio."""
        if not model:
            return None
            
        return MonedaEntity(
            id=model.id,
            codigo=model.codigo,
            nombre=model.nombre,
            simbolo=model.simbolo,
            esta_activo=model.esta_activo,
            fecha_creacion=model.fecha_creacion,
            fecha_actualizacion=model.fecha_actualizacion
        )
    
    @staticmethod
    def to_model(entity: MonedaEntity) -> MonedaModel:
        """Convierte una entidad de Moneda a un modelo de infraestructura."""
        if not entity:
            return None
            
        return MonedaModel(
            id=entity.id,
            codigo=entity.codigo,
            nombre=entity.nombre,
            simbolo=entity.simbolo,
            esta_activo=entity.esta_activo,
            fecha_creacion=entity.fecha_creacion,
            fecha_actualizacion=entity.fecha_actualizacion
        )


class MonedaDTOMapper(DTOMapper):
    """Mapper entre la entidad Moneda y el DTO MonedaDto."""
    
    @staticmethod
    def to_dto(entity: MonedaEntity) -> MonedaDto:
        """Convierte una entidad de Moneda a un DTO."""
        if not entity:
            return None
            
        return MonedaDto(
            id=entity.id,
            codigo=entity.codigo,
            nombre=entity.nombre,
            simbolo=entity.simbolo,
            esta_activo=entity.esta_activo,
            fecha_creacion=entity.fecha_creacion,
            fecha_actualizacion=entity.fecha_actualizacion
        )
    
    @staticmethod
    def to_entity(dto: MonedaDto) -> MonedaEntity:
        """Convierte un DTO a una entidad de Moneda."""
        if not dto:
            return None
            
        return MonedaEntity(
            id=dto.id,
            codigo=dto.codigo,
            nombre=dto.nombre,
            simbolo=dto.simbolo,
            esta_activo=dto.esta_activo,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion
        )


class MonedaSummaryDTOMapper(DTOMapper):
    """Mapper entre la entidad Moneda y el DTO MonedaSummaryDto."""
    
    @staticmethod
    def to_dto(entity: MonedaEntity) -> MonedaSummaryDto:
        """Convierte una entidad de Moneda a un DTO de resumen."""
        if not entity:
            return None
            
        return MonedaSummaryDto(
            id=entity.id,
            codigo=entity.codigo,
            simbolo=entity.simbolo
        )
    
    @staticmethod
    def to_entity(dto: MonedaSummaryDto) -> MonedaEntity:
        """Convierte un DTO de resumen a una entidad de Moneda."""
        if not dto:
            return None
            
        return MonedaEntity(
            id=dto.id,
            codigo=dto.codigo,
            simbolo=dto.simbolo,
            nombre="",  # Valor por defecto ya que el DTO no tiene este campo
            esta_activo=True  # Valor por defecto
        )


class CrearMonedaCommandMapper(DTOMapper):
    """Mapper entre la entidad Moneda y el comando CrearMonedaCommand."""
    
    @staticmethod
    def to_entity(command: CrearMonedaCommand) -> MonedaEntity:
        """Convierte un comando de creación a una entidad de Moneda."""
        if not command:
            return None
            
        return MonedaEntity(
            codigo=command.codigo,
            nombre=command.nombre,
            simbolo=command.simbolo,
            esta_activo=True  # Valor por defecto para nuevas monedas
        )
    
    @staticmethod
    def to_dto(entity: MonedaEntity) -> CrearMonedaCommand:
        """Convierte una entidad de Moneda a un comando de creación."""
        if not entity:
            return None
            
        return CrearMonedaCommand(
            codigo=entity.codigo,
            nombre=entity.nombre,
            simbolo=entity.simbolo
        )
