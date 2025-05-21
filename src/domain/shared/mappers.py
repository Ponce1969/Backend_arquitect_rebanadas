from typing import TypeVar, Generic, List

# Definición de tipos genéricos para entidades y modelos
T = TypeVar('T')  # Tipo para entidades de dominio
M = TypeVar('M')  # Tipo para modelos de infraestructura
D = TypeVar('D')  # Tipo para DTOs


class Mapper(Generic[T, M]):
    """Clase base para mappers entre entidades de dominio y modelos de infraestructura."""
    
    @staticmethod
    def to_entity(model: M) -> T:
        """Convierte un modelo de infraestructura a una entidad de dominio."""
        raise NotImplementedError("Debe implementar el método to_entity")
    
    @staticmethod
    def to_model(entity: T) -> M:
        """Convierte una entidad de dominio a un modelo de infraestructura."""
        raise NotImplementedError("Debe implementar el método to_model")
    
    @classmethod
    def to_entity_list(cls, models: List[M]) -> List[T]:
        """Convierte una lista de modelos a una lista de entidades."""
        return [cls.to_entity(model) for model in models]
    
    @classmethod
    def to_model_list(cls, entities: List[T]) -> List[M]:
        """Convierte una lista de entidades a una lista de modelos."""
        return [cls.to_model(entity) for entity in entities]


class DTOMapper(Generic[T, D]):
    """Clase base para mappers entre entidades de dominio y DTOs."""
    
    @staticmethod
    def to_dto(entity: T) -> D:
        """Convierte una entidad de dominio a un DTO."""
        raise NotImplementedError("Debe implementar el método to_dto")
    
    @staticmethod
    def to_entity(dto: D) -> T:
        """Convierte un DTO a una entidad de dominio."""
        raise NotImplementedError("Debe implementar el método to_entity")
    
    @classmethod
    def to_dto_list(cls, entities: List[T]) -> List[D]:
        """Convierte una lista de entidades a una lista de DTOs."""
        return [cls.to_dto(entity) for entity in entities]
    
    @classmethod
    def to_entity_list(cls, dtos: List[D]) -> List[T]:
        """Convierte una lista de DTOs a una lista de entidades."""
        return [cls.to_entity(dto) for dto in dtos]


class ModelDTOMapper(Generic[M, D]):
    """Clase base para mappers directos entre modelos de infraestructura y DTOs."""
    
    @staticmethod
    def to_dto(model: M) -> D:
        """Convierte un modelo de infraestructura a un DTO."""
        raise NotImplementedError("Debe implementar el método to_dto")
    
    @staticmethod
    def to_model(dto: D) -> M:
        """Convierte un DTO a un modelo de infraestructura."""
        raise NotImplementedError("Debe implementar el método to_model")
    
    @classmethod
    def to_dto_list(cls, models: List[M]) -> List[D]:
        """Convierte una lista de modelos a una lista de DTOs."""
        return [cls.to_dto(model) for model in models]
    
    @classmethod
    def to_model_list(cls, dtos: List[D]) -> List[M]:
        """Convierte una lista de DTOs a una lista de modelos."""
        return [cls.to_model(dto) for dto in dtos]
