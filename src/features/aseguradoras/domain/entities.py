from dataclasses import dataclass
from datetime import datetime


@dataclass
class Aseguradora:
    """Entidad de dominio que representa una aseguradora."""
    id: int | None = None
    nombre: str = ""
    identificador_fiscal: str | None = None
    telefono: str | None = None
    direccion: str | None = None
    email: str | None = None
    pagina_web: str | None = None
    esta_activa: bool = True
    observaciones: str | None = None
    fecha_creacion: datetime | None = None
    fecha_actualizacion: datetime | None = None
    # tipos_seguros: List['TipoSeguro'] = field(default_factory=list)  # Comentado hasta implementar TipoSeguro
