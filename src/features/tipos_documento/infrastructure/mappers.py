
from src.features.shared.mappers import Mapper, DTOMapper
from src.features.tipos_documento.domain.entities import TipoDocumento as TipoDocumentoEntity
from src.features.tipos_documento.infrastructure.models import TipoDocumento as TipoDocumentoModel
from src.features.tipos_documento.application.dtos import (
    TipoDocumentoDto,
    CrearTipoDocumentoCommand
)


class TipoDocumentoMapper(Mapper):
    """Mapper entre la entidad TipoDocumento y el modelo TipoDocumentoModel."""
    
    @staticmethod
    def to_entity(model: TipoDocumentoModel) -> TipoDocumentoEntity:
        """Convierte un modelo de TipoDocumento a una entidad de dominio."""
        if not model:
            return None
            
        return TipoDocumentoEntity(
            id=model.id,
            codigo=model.codigo,
            nombre=model.nombre,
            es_default=model.es_default,
            esta_activo=model.esta_activo,
            fecha_creacion=model.fecha_creacion,
            fecha_actualizacion=model.fecha_actualizacion
        )
    
    @staticmethod
    def to_model(entity: TipoDocumentoEntity) -> TipoDocumentoModel:
        """Convierte una entidad de TipoDocumento a un modelo de infraestructura."""
        if not entity:
            return None
            
        return TipoDocumentoModel(
            id=entity.id,
            codigo=entity.codigo,
            nombre=entity.nombre,
            es_default=entity.es_default,
            esta_activo=entity.esta_activo,
            fecha_creacion=entity.fecha_creacion,
            fecha_actualizacion=entity.fecha_actualizacion
        )


class TipoDocumentoDTOMapper(DTOMapper):
    """Mapper entre la entidad TipoDocumento y el DTO TipoDocumentoDto."""
    
    @staticmethod
    def to_dto(entity: TipoDocumentoEntity) -> TipoDocumentoDto:
        """Convierte una entidad de TipoDocumento a un DTO."""
        if not entity:
            return None
            
        return TipoDocumentoDto(
            id=entity.id,
            codigo=entity.codigo,
            nombre=entity.nombre,
            es_default=entity.es_default,
            esta_activo=entity.esta_activo,
            fecha_creacion=entity.fecha_creacion,
            fecha_actualizacion=entity.fecha_actualizacion
        )
    
    @staticmethod
    def to_entity(dto: TipoDocumentoDto) -> TipoDocumentoEntity:
        """Convierte un DTO a una entidad de TipoDocumento."""
        if not dto:
            return None
            
        return TipoDocumentoEntity(
            id=dto.id,
            codigo=dto.codigo,
            nombre=dto.nombre,
            es_default=dto.es_default,
            esta_activo=dto.esta_activo,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion
        )


class CrearTipoDocumentoCommandMapper(DTOMapper):
    """Mapper entre la entidad TipoDocumento y el comando CrearTipoDocumentoCommand."""
    
    @staticmethod
    def to_entity(command: CrearTipoDocumentoCommand) -> TipoDocumentoEntity:
        """Convierte un comando de creaciu00f3n a una entidad de TipoDocumento."""
        if not command:
            return None
            
        return TipoDocumentoEntity(
            codigo=command.codigo,
            nombre=command.nombre,
            es_default=command.es_default,
            esta_activo=True  # Valor por defecto para nuevos tipos de documento
        )
