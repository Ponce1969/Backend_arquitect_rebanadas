from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID


@dataclass
class Cliente:
    """Entidad de dominio que representa un cliente."""
    id: UUID | None = None
    numero_cliente: int | None = None
    nombres: str = ""
    apellidos: str = ""
    tipo_documento_id: int = 0
    numero_documento: str = ""
    fecha_nacimiento: date | None = None
    direccion: str = ""
    localidad: str | None = None
    telefonos: str = ""
    movil: str = ""
    mail: str = ""
    observaciones: str | None = None
    creado_por_id: int = 0
    modificado_por_id: int = 0
    fecha_creacion: datetime | None = None
    fecha_modificacion: datetime | None = None
    # Relaciones - comentadas hasta que se implementen las entidades relacionadas
    # tipo_documento: Optional['TipoDocumento'] = None
    # creado_por_usuario: Optional['Usuario'] = None
    # modificado_por_usuario: Optional['Usuario'] = None
    # corredores_asociados: List['ClienteCorredor'] = field(default_factory=list)
    # movimientos_vigencias: List['MovimientoVigencia'] = field(default_factory=list)
