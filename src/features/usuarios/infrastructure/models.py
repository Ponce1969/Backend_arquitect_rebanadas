from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.features.usuarios.domain.types import Role
from src.infrastructure.database import Base

from ..domain.entities import Usuario as UsuarioEntity


def get_utc_now():
    """Función helper para obtener el tiempo UTC actual"""
    return datetime.now(timezone.utc)


class Usuario(Base):
    """Modelo para la tabla usuarios.
    
    Este modelo representa a los usuarios del sistema. Un usuario puede tener
    diferentes roles (admin, corredor, asistente) y, dependiendo de su rol,
    puede estar asociado o no a un corredor.
    
    Relaciones:
    - Si el rol es 'corredor', debe tener un corredor_numero asociado
    - Si el rol es 'admin' o 'asistente', puede o no tener un corredor_numero
    """

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(64), nullable=False)
    apellido = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(String(20), default="user")  # Roles: "corredor", "admin", etc.
    corredor_numero = Column(
        Integer, ForeignKey("corredores.numero"), nullable=True
    )  # Relación con corredor (usando el número visible del corredor)
    comision_porcentaje = Column(Float, default=0.0)  # Solo aplicable a corredores
    telefono = Column(String(20))  # Teléfono de contacto
    fecha_creacion = Column(DateTime(timezone=True), default=get_utc_now)
    fecha_modificacion = Column(
        DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now
    )

    # Relaciones
    clientes_creados = relationship(
        "Cliente",
        back_populates="creado_por_usuario",
        foreign_keys="Cliente.creado_por_id",
        lazy="selectin",
    )
    clientes_modificados = relationship(
        "Cliente",
        back_populates="modificado_por_usuario",
        foreign_keys="Cliente.modificado_por_id",
        lazy="selectin",
    )
    corredor_rel = relationship(
        "Corredor",
        back_populates="usuarios",
        lazy="selectin",
    )
    
    def to_entity(self) -> UsuarioEntity:
        """Convierte el modelo SQLAlchemy a Entidad de Dominio."""
        # Mapear el string del rol al Enum del Dominio
        try:
            role_enum = Role(self.role)  # Convertir string a Enum
        except ValueError:
            # Manejar caso si el string de rol en DB no es válido según el Enum
            role_enum = Role.CORREDOR  # O un rol por defecto de error

        return UsuarioEntity(
            id=self.id,
            nombre=self.nombre,
            apellido=self.apellido,
            email=self.email,
            username=self.username,
            # hashed_password NO se mapea a la entidad de dominio
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            role=role_enum,  # Asigna el Enum de Dominio
            corredor_numero=self.corredor_numero,
            comision_porcentaje=self.comision_porcentaje,
            telefono=self.telefono,
            fecha_creacion=self.fecha_creacion,
            fecha_modificacion=self.fecha_modificacion
        )

    @staticmethod
    def from_entity(usuario: UsuarioEntity, hashed_password: str = None) -> 'Usuario':
        """Convierte una Entidad de Dominio a Modelo SQLAlchemy.
        
        Args:
            usuario: Entidad de dominio Usuario
            hashed_password: Contraseña hasheada (requerida para nuevos usuarios)
        """
        model = Usuario(
            id=usuario.id,  # ID para update/delete
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            email=usuario.email,
            username=usuario.username,
            is_active=usuario.is_active,
            is_superuser=usuario.is_superuser,
            role=usuario.role.value,  # Mapea el Enum de Dominio a string para DB
            corredor_numero=usuario.corredor_numero,
            comision_porcentaje=usuario.comision_porcentaje,
            telefono=usuario.telefono,
            fecha_creacion=usuario.fecha_creacion,
            fecha_modificacion=usuario.fecha_modificacion,
        )
        
        # Asignar la contraseña hasheada si se proporciona
        if hashed_password is not None:
            model.hashed_password = hashed_password
            
        return model
