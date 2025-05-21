from datetime import datetime, date, timezone
from typing import Optional


def get_utc_now() -> datetime:
    """Obtiene la fecha y hora actual en UTC.
    
    Returns:
        datetime: Fecha y hora actual en UTC.
    """
    return datetime.now(timezone.utc)


def get_today() -> date:
    """Obtiene la fecha actual.
    
    Returns:
        date: Fecha actual.
    """
    return date.today()


def is_future_date(check_date: date) -> bool:
    """Verifica si una fecha es futura.
    
    Args:
        check_date: Fecha a verificar.
        
    Returns:
        bool: True si la fecha es futura, False en caso contrario.
    """
    return check_date > get_today()


def format_date(dt: Optional[date]) -> Optional[str]:
    """Formatea una fecha en formato ISO (YYYY-MM-DD).
    
    Args:
        dt: Fecha a formatear.
        
    Returns:
        str: Fecha formateada o None si la fecha es None.
    """
    if dt is None:
        return None
    return dt.isoformat()


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Formatea una fecha y hora en formato ISO (YYYY-MM-DDTHH:MM:SS.mmmmmm+00:00).
    
    Args:
        dt: Fecha y hora a formatear.
        
    Returns:
        str: Fecha y hora formateada o None si la fecha y hora es None.
    """
    if dt is None:
        return None
    return dt.isoformat()
