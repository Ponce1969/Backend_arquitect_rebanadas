from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from src.infrastructure.database.base import Base
from src.features.tipos_documento.domain.entities import TipoDocumento as TipoDocumentoEntity


class TipoDocumento(Base):
    """Modelo SQLAlchemy para la tabla tipos_documento."""
    __tablename__ = "tipos_documento"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10), nullable=False, unique=True)  # Codigo u00fanico (ej: DNI, RUT)
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
