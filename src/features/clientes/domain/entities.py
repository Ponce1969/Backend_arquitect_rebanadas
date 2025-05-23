from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID

# Importamos la entidad TipoDocumento del dominio compartido
from src.features.tipos_documento.domain.entities import TipoDocumento


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
    # Relaciones
    tipo_documento: TipoDocumento | None = None
    # creado_por_usuario: Optional['Usuario'] = None
    # modificado_por_usuario: Optional['Usuario'] = None
    corredores_asociados: list[object] = field(default_factory=list)  # Tipo 'ClienteCorredor'
    movimientos_vigencias: list[object] = field(default_factory=list)  # Tipo 'MovimientoVigencia'
