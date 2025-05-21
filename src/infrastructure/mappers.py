from typing import List, Any, Dict, Optional

# Definir tipos genericos para entidades y modelos
T = Any  # Tipo para entidades
M = Any  # Tipo para modelos
D = Any  # Tipo para DTOs


class Mapper:
    """Clase base para mappers entre entidades y modelos."""
    
    @classmethod
    def to_entity(cls, model: M) -> T:
        """Convierte un modelo a una entidad."""
        raise NotImplementedError("El metodo to_entity debe ser implementado por las subclases")
    
    @classmethod
    def to_entity_list(cls, models: List[M]) -> List[T]:
        """Convierte una lista de modelos a una lista de entidades."""
        return [cls.to_entity(model) for model in models] if models else []
    
    @classmethod
    def to_model(cls, entity: T) -> M:
        """Convierte una entidad a un modelo."""
        raise NotImplementedError("El metodo to_model debe ser implementado por las subclases")
    
    @classmethod
    def to_model_list(cls, entities: List[T]) -> List[M]:
        """Convierte una lista de entidades a una lista de modelos."""
        return [cls.to_model(entity) for entity in entities] if entities else []


class DTOMapper:
    """Clase base para mappers entre entidades y DTOs."""
    
    @classmethod
    def to_dto(cls, entity: T) -> D:
        """Convierte una entidad a un DTO."""
        raise NotImplementedError("El metodo to_dto debe ser implementado por las subclases")
    
    @classmethod
    def to_dto_list(cls, entities: List[T]) -> List[D]:
        """Convierte una lista de entidades a una lista de DTOs."""
        return [cls.to_dto(entity) for entity in entities] if entities else []
    
    @classmethod
    def to_entity(cls, dto: D) -> T:
        """Convierte un DTO a una entidad."""
        raise NotImplementedError("El metodo to_entity debe ser implementado por las subclases")
    
    @classmethod
    def to_entity_list(cls, dtos: List[D]) -> List[T]:
        """Convierte una lista de DTOs a una lista de entidades."""
        return [cls.to_entity(dto) for dto in dtos] if dtos else []
