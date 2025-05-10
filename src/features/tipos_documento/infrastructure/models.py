from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from src.infrastructure.database import Base
from src.features.tipos_documento.domain.entities import TipoDocumento as TipoDocumentoEntity


class TipoDocumento(Base):
    """Modelo para la tabla tipos_documento."""
    
    __tablename__ = "tipos_documento"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    clientes = relationship("Cliente", back_populates="tipo_documento_rel", lazy="selectin")
    
    def to_entity(self) -> TipoDocumentoEntity:
        """Convierte el modelo SQLAlchemy a entidad de dominio."""
        return TipoDocumentoEntity(
            id=self.id,
            nombre=self.nombre,
            descripcion=self.descripcion,
            activo=self.activo,
            clientes=[cliente.to_entity() for cliente in self.clientes] if self.clientes else []
        )
    
    @staticmethod
    def from_entity(entity: TipoDocumentoEntity) -> 'TipoDocumento':
        """Convierte una entidad de dominio a modelo SQLAlchemy."""
        return TipoDocumento(
            id=entity.id,
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            activo=entity.activo
        )
