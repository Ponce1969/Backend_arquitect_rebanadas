from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

# Importamos la Base desde la infraestructura compartida
from src.infrastructure.database.base import Base

# Importamos las Entidades de Dominio para mapear
from src.domain.shared.entities import Moneda as MonedaEntity, TipoDocumento as TipoDocumentoEntity


# Definiu00f3n de la funciu00f3n helper para el tiempo
def get_utc_now():
    """Funciu00f3n helper para obtener el tiempo UTC actual en UTC."""
    return datetime.now(timezone.utc)


class Moneda(Base):
    """Modelo SQLAlchemy para la tabla monedas."""
    __tablename__ = "monedas"
    
    id = Column(Integer, primary_key=True)
    codigo = Column(String(10), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    simbolo = Column(String(5), nullable=False)
    esta_activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), default=get_utc_now)
    fecha_actualizacion = Column(
        DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now
    )
    
    # Relaciones
    # movimientos = relationship("MovimientoVigencia", back_populates="moneda_rel")
    
    # Mu00e9todos para mapear entre Modelo SQLAlchemy y Entidad de Dominio
    def to_entity(self) -> MonedaEntity:
        """Convierte el modelo SQLAlchemy a Entidad de Dominio."""
        return MonedaEntity(
            id=self.id,
            codigo=self.codigo,
            nombre=self.nombre,
            simbolo=self.simbolo,
            esta_activo=self.esta_activo,
            fecha_creacion=self.fecha_creacion,
            fecha_actualizacion=self.fecha_actualizacion
        )
    
    @staticmethod
    def from_entity(moneda: MonedaEntity) -> 'Moneda':
        """Convierte una Entidad de Dominio a Modelo SQLAlchemy."""
        return Moneda(
            id=moneda.id,
            codigo=moneda.codigo,
            nombre=moneda.nombre,
            simbolo=moneda.simbolo,
            esta_activo=moneda.esta_activo,
            fecha_creacion=moneda.fecha_creacion,
            fecha_actualizacion=moneda.fecha_actualizacion
        )


class TipoDocumento(Base):
    """Modelo SQLAlchemy para la tabla tipos_documento."""
    __tablename__ = "tipos_documento"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10), nullable=False, unique=True)  # Cu00f3digo u00fanico (ej: DNI, RUT)
    nombre = Column(String(50), nullable=False)  # Nombre completo
    descripcion = Column(String(200))  # Descripciu00f3n adicional
    es_default = Column(Boolean, default=False)  # Indica si es el tipo por defecto
    esta_activo = Column(Boolean, default=True)  # Indica si estu00e1 activo
    
    # Relaciones
    clientes = relationship("Cliente", back_populates="tipo_documento_rel", lazy="selectin")
    
    # Mu00e9todos para mapear entre Modelo SQLAlchemy y Entidad de Dominio
    def to_entity(self) -> TipoDocumentoEntity:
        """Convierte el modelo SQLAlchemy a Entidad de Dominio."""
        return TipoDocumentoEntity(
            id=self.id,
            codigo=self.codigo,
            nombre=self.nombre,
            descripcion=self.descripcion,
            es_default=self.es_default,
            esta_activo=self.esta_activo
        )
    
    @staticmethod
    def from_entity(tipo_documento: TipoDocumentoEntity) -> 'TipoDocumento':
        """Convierte una Entidad de Dominio a Modelo SQLAlchemy."""
        return TipoDocumento(
            id=tipo_documento.id,
            codigo=tipo_documento.codigo,
            nombre=tipo_documento.nombre,
            descripcion=tipo_documento.descripcion,
            es_default=tipo_documento.es_default,
            esta_activo=tipo_documento.esta_activo
        )