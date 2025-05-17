from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar
import time

# Definimos tipos para el tipado
T = TypeVar('T')
CacheKey = str
CacheValue = Any
CacheDict = Dict[CacheKey, tuple[CacheValue, float]]

# Cache en memoria simple
_cache: CacheDict = {}

# Tiempo de expiraciu00f3n por defecto en segundos (5 minutos)
DEFAULT_EXPIRY = 300


def get_cache(key: CacheKey) -> Optional[CacheValue]:
    """Obtiene un valor de la cachu00e9 si existe y no ha expirado."""
    if key not in _cache:
        return None
    
    value, expiry = _cache[key]
    if time.time() > expiry:
        # El valor ha expirado, lo eliminamos
        del _cache[key]
        return None
    
    return value


def set_cache(key: CacheKey, value: CacheValue, expiry_seconds: int = DEFAULT_EXPIRY) -> None:
    """Guarda un valor en la cachu00e9 con un tiempo de expiraciu00f3n."""
    _cache[key] = (value, time.time() + expiry_seconds)


def clear_cache(prefix: Optional[str] = None) -> None:
    """Limpia la cachu00e9 completa o solo las claves que comienzan con un prefijo."""
    global _cache
    
    if prefix is None:
        _cache = {}
    else:
        keys_to_delete = [k for k in _cache.keys() if k.startswith(prefix)]
        for key in keys_to_delete:
            del _cache[key]


def cached(expiry_seconds: int = DEFAULT_EXPIRY, key_prefix: str = ""):
    """Decorador para cachear el resultado de una funciu00f3n."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Generamos una clave u00fanica basada en la funciu00f3n y sus argumentos
            cache_key = f"{key_prefix}{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Intentamos obtener el resultado de la cachu00e9
            cached_result = get_cache(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Si no estu00e1 en cachu00e9, ejecutamos la funciu00f3n
            result = func(*args, **kwargs)
            
            # Guardamos el resultado en cachu00e9
            set_cache(cache_key, result, expiry_seconds)
            
            return result
        return wrapper
    return decorator
