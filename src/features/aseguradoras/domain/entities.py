from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Aseguradora:
    """Entidad de dominio que representa una aseguradora."""
    id: Optional[int] = None
    nombre: str = ""
    identificador_fiscal: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[str] = None
    pagina_web: Optional[str] = None
    esta_activa: bool = True
    observaciones: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    # tipos_seguros: List['TipoSeguro'] = field(default_factory=list)  # Comentado hasta implementar TipoSeguro
