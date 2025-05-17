import pytest
from datetime import datetime, timezone

from src.features.monedas.domain.entities import Moneda as MonedaEntity
from src.features.monedas.infrastructure.models import Moneda as MonedaModel
from src.features.monedas.application.dtos import MonedaDto, MonedaSummaryDto, CrearMonedaCommand
from src.features.monedas.infrastructure.mappers import (
    MonedaMapper,
    MonedaDTOMapper,
    MonedaSummaryDTOMapper,
    CrearMonedaCommandMapper
)


@pytest.fixture
def moneda_entity():
    """Fixture que devuelve una entidad Moneda para pruebas."""
    return MonedaEntity(
        id=1,
        codigo="USD",
        nombre="Dolar Estadounidense",
        simbolo="$",
        esta_activo=True,
        fecha_creacion=datetime.now(timezone.utc),
        fecha_actualizacion=datetime.now(timezone.utc)
    )


@pytest.fixture
def moneda_model(moneda_entity):
    """Fixture que devuelve un modelo Moneda para pruebas."""
    return MonedaModel(
        id=moneda_entity.id,
        codigo=moneda_entity.codigo,
        nombre=moneda_entity.nombre,
        simbolo=moneda_entity.simbolo,
        esta_activo=moneda_entity.esta_activo,
        fecha_creacion=moneda_entity.fecha_creacion,
        fecha_actualizacion=moneda_entity.fecha_actualizacion
    )


@pytest.fixture
def moneda_dto(moneda_entity):
    """Fixture que devuelve un DTO Moneda para pruebas."""
    return MonedaDto(
        id=moneda_entity.id,
        codigo=moneda_entity.codigo,
        nombre=moneda_entity.nombre,
        simbolo=moneda_entity.simbolo,
        esta_activo=moneda_entity.esta_activo,
        fecha_creacion=moneda_entity.fecha_creacion,
        fecha_actualizacion=moneda_entity.fecha_actualizacion
    )


@pytest.fixture
def crear_moneda_command():
    """Fixture que devuelve un comando CrearMoneda para pruebas."""
    return CrearMonedaCommand(
        codigo="EUR",
        nombre="Euro",
        simbolo="u20ac"
    )


class TestMonedaMapper:
    """Pruebas para el mapper entre entidad y modelo de Moneda."""

    def test_to_entity(self, moneda_model):
        """Prueba la conversión de modelo a entidad."""
        entity = MonedaMapper.to_entity(moneda_model)
        
        assert entity is not None
        assert entity.id == moneda_model.id
        assert entity.codigo == moneda_model.codigo
        assert entity.nombre == moneda_model.nombre
        assert entity.simbolo == moneda_model.simbolo
        assert entity.esta_activo == moneda_model.esta_activo
        assert entity.fecha_creacion == moneda_model.fecha_creacion
        assert entity.fecha_actualizacion == moneda_model.fecha_actualizacion

    def test_to_model(self, moneda_entity):
        """Prueba la conversión de entidad a modelo."""
        model = MonedaMapper.to_model(moneda_entity)
        
        assert model is not None
        assert model.id == moneda_entity.id
        assert model.codigo == moneda_entity.codigo
        assert model.nombre == moneda_entity.nombre
        assert model.simbolo == moneda_entity.simbolo
        assert model.esta_activo == moneda_entity.esta_activo
        assert model.fecha_creacion == moneda_entity.fecha_creacion
        assert model.fecha_actualizacion == moneda_entity.fecha_actualizacion

    def test_to_entity_list(self, moneda_model):
        """Prueba la conversión de lista de modelos a lista de entidades."""
        models = [moneda_model, moneda_model]
        entities = MonedaMapper.to_entity_list(models)
        
        assert len(entities) == 2
        for entity in entities:
            assert entity.id == moneda_model.id
            assert entity.codigo == moneda_model.codigo

    def test_to_model_list(self, moneda_entity):
        """Prueba la conversión de lista de entidades a lista de modelos."""
        entities = [moneda_entity, moneda_entity]
        models = MonedaMapper.to_model_list(entities)
        
        assert len(models) == 2
        for model in models:
            assert model.id == moneda_entity.id
            assert model.codigo == moneda_entity.codigo


class TestMonedaDTOMapper:
    """Pruebas para el mapper entre entidad y DTO de Moneda."""

    def test_to_dto(self, moneda_entity):
        """Prueba la conversión de entidad a DTO."""
        dto = MonedaDTOMapper.to_dto(moneda_entity)
        
        assert dto is not None
        assert dto.id == moneda_entity.id
        assert dto.codigo == moneda_entity.codigo
        assert dto.nombre == moneda_entity.nombre
        assert dto.simbolo == moneda_entity.simbolo
        assert dto.esta_activo == moneda_entity.esta_activo
        assert dto.fecha_creacion == moneda_entity.fecha_creacion
        assert dto.fecha_actualizacion == moneda_entity.fecha_actualizacion

    def test_to_entity(self, moneda_dto):
        """Prueba la conversión de DTO a entidad."""
        entity = MonedaDTOMapper.to_entity(moneda_dto)
        
        assert entity is not None
        assert entity.id == moneda_dto.id
        assert entity.codigo == moneda_dto.codigo
        assert entity.nombre == moneda_dto.nombre
        assert entity.simbolo == moneda_dto.simbolo
        assert entity.esta_activo == moneda_dto.esta_activo
        assert entity.fecha_creacion == moneda_dto.fecha_creacion
        assert entity.fecha_actualizacion == moneda_dto.fecha_actualizacion


class TestCrearMonedaCommandMapper:
    """Pruebas para el mapper entre comando de creación y entidad de Moneda."""

    def test_to_entity(self, crear_moneda_command):
        """Prueba la conversión de comando a entidad."""
        entity = CrearMonedaCommandMapper.to_entity(crear_moneda_command)
        
        assert entity is not None
        assert entity.id is None  # ID no se establece en la creación
        assert entity.codigo == crear_moneda_command.codigo
        assert entity.nombre == crear_moneda_command.nombre
        assert entity.simbolo == crear_moneda_command.simbolo
        assert entity.esta_activo is True  # Valor por defecto
