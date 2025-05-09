from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List, UUID


@dataclass
class Cliente:
    """Entidad de dominio que representa un cliente."""
    id: Optional[UUID] = None
    numero_cliente: Optional[int] = None
    nombres: str = ""
    apellidos: str = ""
    tipo_documento_id: int = 0
    numero_documento: str = ""
    fecha_nacimiento: Optional[date] = None
    direccion: str = ""
    localidad: Optional[str] = None
    telefonos: str = ""
    movil: str = ""
    mail: str = ""
    observaciones: Optional[str] = None
    creado_por_id: int = 0
    modificado_por_id: int = 0
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
    # Relaciones - comentadas hasta que se implementen las entidades relacionadas
    # tipo_documento: Optional['TipoDocumento'] = None
    # creado_por_usuario: Optional['Usuario'] = None
    # modificado_por_usuario: Optional['Usuario'] = None
    # corredores_asociados: List['ClienteCorredor'] = field(default_factory=list)
    # movimientos_vigencias: List['MovimientoVigencia'] = field(default_factory=list)
