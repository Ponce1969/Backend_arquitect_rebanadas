from datetime import datetime, timedelta
from typing import Any

# Intentamos importar PyJWT de diferentes formas para mayor compatibilidad
try:
    import jwt
    from jwt.exceptions import PyJWTError
except ImportError:
    try:
        import PyJWT as jwt
        from jwt.exceptions import PyJWTError
    except ImportError:
        from python_jose import jwt
        from python_jose.exceptions import JWTError as PyJWTError

from src.config.settings import settings


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Crea un token JWT de acceso.
    
    Args:
        data: Datos a incluir en el token (payload)
        expires_delta: Tiempo de expiración opcional
        
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    
    # Establecer tiempo de expiración
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Agregar claims estándar
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access_token"
    })
    
    # Codificar token con la clave secreta
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any] | None:
    """
    Decodifica y valida un token JWT.
    
    Args:
        token: Token JWT a decodificar
        
    Returns:
        Payload del token si es válido, None en caso contrario
    """
    try:
        # Decodificar token
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # Verificar que sea un token de acceso
        if payload.get("type") != "access_token":
            return None
        
        return payload
    except PyJWTError:
        # Cualquier error de JWT (expirado, firma inválida, etc.)
        return None
