import pytest
from unittest.mock import MagicMock, patch

from src.features.monedas.domain.entities import Moneda as MonedaEntity
from src.features.monedas.domain.exceptions import MonedaNotFoundException, MonedaCodigoExistsException
from src.features.monedas.infrastructure.models import Moneda as MonedaModel
from src.features.monedas.infrastructure.repositories import SQLAlchemyMonedaRepository
from src.features.monedas.infrastructure.mappers import MonedaMapper


@pytest.fixture
def moneda_entity():
    """Fixture que devuelve una entidad Moneda para pruebas."""
    return MonedaEntity(
        id=1,
        codigo="USD",
        nombre="Dolar Estadounidense",
        simbolo="$",
        esta_activo=True
    )


@pytest.fixture
def moneda_model(moneda_entity):
    """Fixture que devuelve un modelo Moneda para pruebas."""
    model = MonedaModel(
        id=moneda_entity.id,
        codigo=moneda_entity.codigo,
        nombre=moneda_entity.nombre,
        simbolo=moneda_entity.simbolo,
        esta_activo=moneda_entity.esta_activo
    )
    return model


@pytest.fixture
def mock_session():
    """Fixture que devuelve una sesion mock para pruebas."""
    session = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = None
    return session


class TestSQLAlchemyMonedaRepository:
    """Pruebas para el repositorio SQLAlchemy de Moneda."""

    def test_get_by_id_found(self, mock_session, moneda_model, moneda_entity):
        """Prueba que get_by_id devuelve la entidad correcta cuando encuentra la moneda."""
        # Configurar el mock para que devuelva el modelo
        mock_session.query.return_value.filter.return_value.first.return_value = moneda_model
        
        # Crear el repositorio con la sesion mock
        repo = SQLAlchemyMonedaRepository(mock_session)
        
        # Llamar al metodo y verificar el resultado
        with patch('src.features.monedas.infrastructure.mappers.MonedaMapper.to_entity', return_value=moneda_entity) as mock_to_entity:
            result = repo.get_by_id(1)
            
            # Verificar que se llamó al mapper correctamente
            mock_to_entity.assert_called_once_with(moneda_model)
            
            # Verificar que el resultado es la entidad esperada
            assert result == moneda_entity
            
            # Verificar que se llamó a la consulta correcta
            mock_session.query.assert_called_once()
            mock_session.query.return_value.filter.assert_called_once()

    def test_get_by_id_not_found(self, mock_session):
        """Prueba que get_by_id lanza NotFoundError cuando no encuentra la moneda."""
        # Configurar el mock para que devuelva None
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        # Crear el repositorio con la sesion mock
        repo = SQLAlchemyMonedaRepository(mock_session)
        
        # Verificar que se lanza la excepcion correcta
        with pytest.raises(MonedaNotFoundException):
            repo.get_by_id(1)

    def test_add_success(self, mock_session, moneda_entity, moneda_model):
        """Prueba que add guarda correctamente la entidad."""
        # Configurar el mock para que no encuentre monedas existentes con el mismo codigo
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        # Crear el repositorio con la sesion mock
        repo = SQLAlchemyMonedaRepository(mock_session)
        
        # Configurar los mocks para los mappers
        with patch('src.features.monedas.infrastructure.mappers.MonedaMapper.to_model', return_value=moneda_model) as mock_to_model, \
             patch('src.features.monedas.infrastructure.mappers.MonedaMapper.to_entity', return_value=moneda_entity) as mock_to_entity, \
             patch('src.infrastructure.cache.clear_cache') as mock_clear_cache:
            
            result = repo.add(moneda_entity)
            
            # Verificar que se llamó a los mappers correctamente
            mock_to_model.assert_called_once_with(moneda_entity)
            mock_to_entity.assert_called_once_with(moneda_model)
            
            # Verificar que se agregó el modelo a la sesion
            mock_session.add.assert_called_once_with(moneda_model)
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once_with(moneda_model)
            
            # Verificar que se limpió la caché
            assert mock_clear_cache.call_count == 2
            
            # Verificar que el resultado es la entidad esperada
            assert result == moneda_entity

    def test_add_duplicate_codigo(self, mock_session, moneda_entity):
        """Prueba que add lanza MonedaCodigoExistsException cuando ya existe una moneda con el mismo codigo."""
        # Configurar el mock para que encuentre una moneda existente con el mismo codigo
        mock_session.query.return_value.filter.return_value.first.return_value = MonedaModel()
        
        # Crear el repositorio con la sesion mock
        repo = SQLAlchemyMonedaRepository(mock_session)
        
        # Verificar que se lanza la excepcion correcta
        with pytest.raises(MonedaCodigoExistsException):
            repo.add(moneda_entity)
