import pytest
from unittest.mock import MagicMock, patch

from src.features.monedas.domain.entities import Moneda as MonedaEntity
from src.features.monedas.application.dtos import MonedaDto, CrearMonedaCommand, ActualizarMonedaCommand
from src.features.monedas.application.use_cases import (
    ObtenerMonedaUseCase,
    ObtenerMonedaPorCodigoUseCase,
    ListarMonedasUseCase,
    CrearMonedaUseCase,
    ActualizarMonedaUseCase,
    EliminarMonedaUseCase
)
from src.features.monedas.infrastructure.mappers import MonedaDTOMapper, CrearMonedaCommandMapper


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
def moneda_dto(moneda_entity):
    """Fixture que devuelve un DTO Moneda para pruebas."""
    return MonedaDto(
        id=moneda_entity.id,
        codigo=moneda_entity.codigo,
        nombre=moneda_entity.nombre,
        simbolo=moneda_entity.simbolo,
        esta_activo=moneda_entity.esta_activo
    )


@pytest.fixture
def crear_moneda_command():
    """Fixture que devuelve un comando CrearMoneda para pruebas."""
    return CrearMonedaCommand(
        codigo="EUR",
        nombre="Euro",
        simbolo="u20ac"
    )


@pytest.fixture
def actualizar_moneda_command():
    """Fixture que devuelve un comando ActualizarMoneda para pruebas."""
    return ActualizarMonedaCommand(
        id=1,
        codigo="USD",
        nombre="Dolar Americano",  # Nombre actualizado
        simbolo="$"
    )


@pytest.fixture
def mock_repository():
    """Fixture que devuelve un repositorio mock para pruebas."""
    return MagicMock()


class TestObtenerMonedaUseCase:
    """Pruebas para el caso de uso ObtenerMonedaUseCase."""

    def test_execute(self, mock_repository, moneda_entity, moneda_dto):
        """Prueba que execute devuelve el DTO correcto."""
        # Configurar el mock para que devuelva la entidad
        mock_repository.get_by_id.return_value = moneda_entity
        
        # Crear el caso de uso con el repositorio mock
        use_case = ObtenerMonedaUseCase(mock_repository)
        
        # Llamar al metodo y verificar el resultado
        with patch('src.features.monedas.infrastructure.mappers.MonedaDTOMapper.to_dto', return_value=moneda_dto) as mock_to_dto:
            result = use_case.execute(1)
            
            # Verificar que se llamó al mapper correctamente
            mock_to_dto.assert_called_once_with(moneda_entity)
            
            # Verificar que el resultado es el DTO esperado
            assert result == moneda_dto
            
            # Verificar que se llamó al repositorio correctamente
            mock_repository.get_by_id.assert_called_once_with(1)


class TestListarMonedasUseCase:
    """Pruebas para el caso de uso ListarMonedasUseCase."""

    def test_execute(self, mock_repository, moneda_entity, moneda_dto):
        """Prueba que execute devuelve la lista de DTOs correcta."""
        # Configurar el mock para que devuelva una lista de entidades
        mock_repository.get_all.return_value = [moneda_entity, moneda_entity]
        
        # Crear el caso de uso con el repositorio mock
        use_case = ListarMonedasUseCase(mock_repository)
        
        # Llamar al metodo y verificar el resultado
        with patch('src.features.monedas.infrastructure.mappers.MonedaDTOMapper.to_dto_list', return_value=[moneda_dto, moneda_dto]) as mock_to_dto_list:
            result = use_case.execute()
            
            # Verificar que se llamó al mapper correctamente
            mock_to_dto_list.assert_called_once_with([moneda_entity, moneda_entity])
            
            # Verificar que el resultado es la lista de DTOs esperada
            assert result == [moneda_dto, moneda_dto]
            
            # Verificar que se llamó al repositorio correctamente
            mock_repository.get_all.assert_called_once()


class TestCrearMonedaUseCase:
    """Pruebas para el caso de uso CrearMonedaUseCase."""

    def test_execute(self, mock_repository, crear_moneda_command, moneda_entity, moneda_dto):
        """Prueba que execute crea correctamente la moneda y devuelve el DTO."""
        # Configurar el mock para que devuelva la entidad creada
        mock_repository.add.return_value = moneda_entity
        
        # Crear el caso de uso con el repositorio mock
        use_case = CrearMonedaUseCase(mock_repository)
        
        # Llamar al metodo y verificar el resultado
        with patch('src.features.monedas.infrastructure.mappers.CrearMonedaCommandMapper.to_entity', return_value=moneda_entity) as mock_command_to_entity, \
             patch('src.features.monedas.infrastructure.mappers.MonedaDTOMapper.to_dto', return_value=moneda_dto) as mock_to_dto:
            
            result = use_case.execute(crear_moneda_command)
            
            # Verificar que se llamaron a los mappers correctamente
            mock_command_to_entity.assert_called_once_with(crear_moneda_command)
            mock_to_dto.assert_called_once_with(moneda_entity)
            
            # Verificar que el resultado es el DTO esperado
            assert result == moneda_dto
            
            # Verificar que se llamó al repositorio correctamente
            mock_repository.add.assert_called_once_with(moneda_entity)


class TestActualizarMonedaUseCase:
    """Pruebas para el caso de uso ActualizarMonedaUseCase."""

    def test_execute(self, mock_repository, actualizar_moneda_command, moneda_entity, moneda_dto):
        """Prueba que execute actualiza correctamente la moneda y devuelve el DTO."""
        # Configurar el mock para que devuelva la entidad original y la actualizada
        mock_repository.get_by_id.return_value = moneda_entity
        mock_repository.update.return_value = moneda_entity
        
        # Crear el caso de uso con el repositorio mock
        use_case = ActualizarMonedaUseCase(mock_repository)
        
        # Llamar al metodo y verificar el resultado
        with patch('src.features.monedas.infrastructure.mappers.MonedaDTOMapper.to_dto', return_value=moneda_dto) as mock_to_dto:
            result = use_case.execute(actualizar_moneda_command)
            
            # Verificar que se llamó al mapper correctamente
            mock_to_dto.assert_called_once_with(moneda_entity)
            
            # Verificar que el resultado es el DTO esperado
            assert result == moneda_dto
            
            # Verificar que se llamaron a los metodos del repositorio correctamente
            mock_repository.get_by_id.assert_called_once_with(actualizar_moneda_command.id)
            mock_repository.update.assert_called_once()


class TestEliminarMonedaUseCase:
    """Pruebas para el caso de uso EliminarMonedaUseCase."""

    def test_execute(self, mock_repository):
        """Prueba que execute elimina correctamente la moneda."""
        # Configurar el mock para que devuelva True
        mock_repository.delete.return_value = True
        
        # Crear el caso de uso con el repositorio mock
        use_case = EliminarMonedaUseCase(mock_repository)
        
        # Llamar al metodo y verificar el resultado
        result = use_case.execute(1)
        
        # Verificar que el resultado es True
        assert result is True
        
        # Verificar que se llamó al repositorio correctamente
        mock_repository.delete.assert_called_once_with(1)
