from datetime import date, datetime, timezone

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

# Importamos la Entidad de Dominio para mapeo
from src.features.sustituciones_corredores.domain.entities import SustitucionCorredor as SustitucionCorredorEntity

# Importamos la Base desde la infraestructura compartida
from src.infrastructure.database import Base


# Definiciu00f3n de la funciu00f3n helper para el tiempo (si no estu00e1 en un util compartido)
def get_utc_now():
    """Funciu00f3n helper para obtener el tiempo UTC actual."""
    return datetime.now(timezone.utc)


# --- Modelo SQLAlchemy para la tabla SustitucionesCorredores ---
class SustitucionCorredor(Base):
    """Modelo SQLAlchemy para la tabla sustituciones_corredores."""

    __tablename__ = "sustituciones_corredores"

    # Identificaciu00f3n
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Clave primaria tu00e9cnica
    
    # Referencias a corredores (por nu00famero, no por ID tu00e9cnico)
    corredor_ausente_numero = Column(Integer, ForeignKey("corredores.numero"), nullable=False, index=True)
    corredor_sustituto_numero = Column(Integer, ForeignKey("corredores.numero"), nullable=False, index=True)
    
    # Fechas de la sustituciu00f3n
    fecha_inicio = Column(Date, nullable=False, index=True)
    fecha_fin = Column(Date, nullable=True, index=True)  # Puede ser NULL si la sustituciu00f3n no tiene fecha de fin definida
    
    # Estado y detalles
    estado = Column(String(20), default="activa", nullable=False, index=True)  # activa, inactiva
    motivo = Column(String(200), nullable=False)
    observaciones = Column(Text, nullable=True)
    
    # Auditoru00eda
    fecha_creacion = Column(DateTime, default=get_utc_now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=get_utc_now, onupdate=get_utc_now, nullable=False)
    
    # Relaciones
    corredor_ausente = relationship(
        "Corredor", 
        foreign_keys=[corredor_ausente_numero],
        primaryjoin="SustitucionCorredor.corredor_ausente_numero == Corredor.numero",
        backref="sustituciones_como_ausente"
    )
    
    corredor_sustituto = relationship(
        "Corredor", 
        foreign_keys=[corredor_sustituto_numero],
        primaryjoin="SustitucionCorredor.corredor_sustituto_numero == Corredor.numero",
        backref="sustituciones_como_sustituto"
    )
    
    # Mu00e9todos para mapear a Entidad de Dominio
    def to_entity(self) -> SustitucionCorredorEntity:
        """Convierte el modelo SQLAlchemy a Entidad de Dominio."""
        return SustitucionCorredorEntity(
            id=self.id,
            corredor_ausente_numero=self.corredor_ausente_numero,
            corredor_sustituto_numero=self.corredor_sustituto_numero,
            fecha_inicio=self.fecha_inicio,
            fecha_fin=self.fecha_fin,
            estado=self.estado,
            motivo=self.motivo,
            observaciones=self.observaciones,
            fecha_creacion=self.fecha_creacion,
            fecha_actualizacion=self.fecha_actualizacion
        )
    
    @staticmethod
    def from_entity(sustitucion: SustitucionCorredorEntity) -> 'SustitucionCorredor':
        """Convierte una Entidad de Dominio a Modelo SQLAlchemy."""
        return SustitucionCorredor(
            id=sustitucion.id,  # None para nuevas entidades
            corredor_ausente_numero=sustitucion.corredor_ausente_numero,
            corredor_sustituto_numero=sustitucion.corredor_sustituto_numero,
            fecha_inicio=sustitucion.fecha_inicio,
            fecha_fin=sustitucion.fecha_fin,
            estado=sustitucion.estado,
            motivo=sustitucion.motivo,
            observaciones=sustitucion.observaciones
            # No mapeamos fechas de creaciu00f3n/actualizaciu00f3n, se manejan automu00e1ticamente
        )
