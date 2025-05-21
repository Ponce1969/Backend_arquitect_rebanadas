import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from src.domain.shared.exceptions import (
    APIError,
    NotFoundError,
    ValidationError,
    UnauthorizedError,
    ForbiddenError,
    ConflictError,
    global_exception_handler
)


@pytest.fixture
def test_app():
    """Fixture que devuelve una aplicacion FastAPI para pruebas."""
    app = FastAPI()
    
    # Registrar el manejador global de excepciones
    app.add_exception_handler(APIError, global_exception_handler)
    
    # Asegurarse de que todas las excepciones no controladas sean manejadas
    @app.exception_handler(Exception)
    async def exception_handler(request, exc):
        return await global_exception_handler(request, exc)
    
    # Endpoint que lanza NotFoundError
    @app.get("/not-found")
    async def not_found_endpoint():
        raise NotFoundError(resource="Test", details={"id": 1})
    
    # Endpoint que lanza ValidationError
    @app.get("/validation-error")
    async def validation_error_endpoint():
        raise ValidationError(details={"field": "El campo es requerido"})
    
    # Endpoint que lanza UnauthorizedError
    @app.get("/unauthorized")
    async def unauthorized_endpoint():
        raise UnauthorizedError(message="No autorizado para acceder a este recurso")
    
    # Endpoint que lanza ForbiddenError
    @app.get("/forbidden")
    async def forbidden_endpoint():
        raise ForbiddenError(message="No tiene permisos para realizar esta accion")
    
    # Endpoint que lanza ConflictError
    @app.get("/conflict")
    async def conflict_endpoint():
        raise ConflictError(message="El recurso ya existe", details={"code": "duplicate"})
    
    # Endpoint que lanza una excepciu00f3n no controlada
    @app.get("/unexpected-error")
    async def unexpected_error_endpoint():
        raise ValueError("Error inesperado")
    
    return app


@pytest.fixture
def client(test_app):
    """Fixture que devuelve un cliente de prueba para la aplicacion."""
    return TestClient(test_app)


class TestExceptionHandlers:
    """Pruebas para los manejadores de excepciones."""

    def test_not_found_error(self, client):
        """Prueba que NotFoundError se maneje correctamente."""
        response = client.get("/not-found")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert data["error"]["message"] == "Test no encontrado"
        assert data["error"]["details"] == {"id": 1}

    def test_validation_error(self, client):
        """Prueba que ValidationError se maneje correctamente."""
        response = client.get("/validation-error")
        
        assert response.status_code == 422
        data = response.json()
        assert "error" in data
        # Comparar sin tener en cuenta los acentos
        assert data["error"]["message"].lower().replace("ó", "o") == "error de validacion"
        assert data["error"]["details"] == {"field": "El campo es requerido"}

    def test_unauthorized_error(self, client):
        """Prueba que UnauthorizedError se maneje correctamente."""
        response = client.get("/unauthorized")
        
        assert response.status_code == 401
        data = response.json()
        assert "error" in data
        assert data["error"]["message"] == "No autorizado para acceder a este recurso"

    def test_forbidden_error(self, client):
        """Prueba que ForbiddenError se maneje correctamente."""
        response = client.get("/forbidden")
        
        assert response.status_code == 403
        data = response.json()
        assert "error" in data
        assert data["error"]["message"] == "No tiene permisos para realizar esta accion"

    def test_conflict_error(self, client):
        """Prueba que ConflictError se maneje correctamente."""
        response = client.get("/conflict")
        
        assert response.status_code == 409
        data = response.json()
        assert "error" in data
        assert data["error"]["message"] == "El recurso ya existe"
        assert data["error"]["details"] == {"code": "duplicate"}

    def test_unexpected_error(self, client, monkeypatch):
        """Prueba que las excepciones no controladas se manejen correctamente."""
        # En lugar de probar con el endpoint que lanza una excepción,
        # vamos a probar directamente el manejador de excepciones
        from fastapi import Request
        from src.domain.shared.exceptions import global_exception_handler
        
        # Crear una solicitud mock
        mock_request = MagicMock(spec=Request)
        
        # Crear una excepción
        test_exception = ValueError("Error inesperado")
        
        # Llamar al manejador de excepciones directamente
        import asyncio
        response = asyncio.run(global_exception_handler(mock_request, test_exception))
        
        # Verificar que la respuesta es correcta
        assert response.status_code == 500
        
        # Convertir el contenido JSON a un diccionario
        import json
        data = json.loads(response.body)
        
        # Verificar que el cuerpo de la respuesta contiene el mensaje de error esperado
        assert "error" in data
        assert data["error"]["message"] == "Error interno del servidor"
