from fastapi import status
from fastapi.responses import JSONResponse

# Excepciones base para toda la aplicaciu00f3n
class APIError(Exception):
    """Excepciu00f3n base para todos los errores de la API"""
    def __init__(self, status_code: int, message: str, details: dict = None):
        self.status_code = status_code
        self.message = message
        self.details = details or {}

class NotFoundError(APIError):
    """Excepciu00f3n para recursos no encontrados"""
    def __init__(self, resource: str, details: dict = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"{resource} no encontrado",
            details=details
        )

class ValidationError(APIError):
    """Excepciu00f3n para errores de validaciu00f3n"""
    def __init__(self, details: dict = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Error de validaciu00f3n",
            details=details
        )

class UnauthorizedError(APIError):
    """Excepciu00f3n para errores de autenticaciu00f3n"""
    def __init__(self, message: str = "No autorizado", details: dict = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            details=details
        )

class ForbiddenError(APIError):
    """Excepciu00f3n para errores de permisos"""
    def __init__(self, message: str = "Acceso denegado", details: dict = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            details=details
        )

class ConflictError(APIError):
    """Excepciu00f3n para conflictos de datos"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            details=details
        )

# Manejador global de excepciones
async def global_exception_handler(request, exc: Exception) -> JSONResponse:
    """Manejador global de excepciones para la aplicaciu00f3n"""
    if isinstance(exc, APIError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )
    
    # Manejo de errores de validaciu00f3n de Pydantic
    if hasattr(exc, "status_code") and exc.status_code == 422:
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "message": "Error de validaciu00f3n",
                    "details": {
                        "errors": exc.errors() if hasattr(exc, "errors") else str(exc)
                    }
                }
            }
        )
    
    # Manejo de errores inesperados
    import logging
    logging.exception("Error inesperado")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Error interno del servidor",
                "details": {}
            }
        }
    )
