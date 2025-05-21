"""
Modelos de base de datos para el módulo de usuarios.

Este módulo contiene las definiciones de los modelos SQLAlchemy utilizados
para interactuar con la base de datos en el contexto de usuarios.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Type, TypeVar

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, event
from sqlalchemy.orm import relationship

from src.config.settings import settings
from src.features.usuarios.domain.types import Role
from src.infrastructure.database import Base
from ..domain.entities import Usuario as UsuarioEntity

# Type variable para métodos de clase
T = TypeVar('T', bound='Usuario')


def get_utc_now() -> datetime:
    """
    Función helper para obtener el tiempo UTC actual.
    
    Returns:
        datetime: Fecha y hora actual en UTC.
    """
    return datetime.now(timezone.utc)


class Usuario(Base):
    """
    Modelo SQLAlchemy para la tabla 'usuarios'.
    
    Este modelo representa a los usuarios del sistema con sus respectivos roles,
    permisos y relaciones con otras entidades como corredores.
    
    Atributos:
        id: Identificador único del usuario
        nombre: Nombre del usuario
        apellido: Apellido del usuario
        email: Correo electrónico (único)
        username: Nombre de usuario (único)
        hashed_password: Contraseña hasheada
        is_active: Indica si la cuenta está activa
        is_superuser: Indica si es superusuario
        role: Rol del usuario (corredor, admin, asistente, etc.)
        corredor_numero: Referencia al corredor asociado (opcional)
        comision_porcentaje: Porcentaje de comisión (para corredores)
        telefono: Número de teléfono de contacto
        fecha_creacion: Fecha de creación del registro
        fecha_modificacion: Fecha de última modificación
        intentos_fallidos: Contador de intentos fallidos de inicio de sesión
        bloqueado_hasta: Fecha hasta la que el usuario está bloqueado
        ultimo_intento_fallido: Fecha del último intento fallido
    """
    __tablename__ = 'usuarios'
    __table_args__ = {
        'comment': 'Tabla que almacena la información de los usuarios del sistema'
    }

    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        comment='Identificador único del usuario'
    )
    nombre = Column(
        String(64), 
        nullable=False,
        comment='Nombre del usuario'
    )
    apellido = Column(
        String(64), 
        nullable=False,
        comment='Apellido del usuario'
    )
    email = Column(
        String(64), 
        nullable=False, 
        unique=True,
        index=True,
        comment='Correo electrónico del usuario (único)'
    )
    username = Column(
        String(64), 
        unique=True, 
        index=True, 
        nullable=False,
        comment='Nombre de usuario único para autenticación'
    )
    hashed_password = Column(
        String(128), 
        nullable=False,
        comment='Hash de la contraseña del usuario'
    )
    is_active = Column(
        Boolean, 
        default=True,
        comment='Indica si la cuenta del usuario está activa'
    )
    is_superuser = Column(
        Boolean, 
        default=False,
        comment='Indica si el usuario tiene privilegios de superusuario'
    )
    role = Column(
        String(20), 
        default=Role.ASISTENTE.value,
        nullable=False,
        comment='Rol del usuario en el sistema (admin, corredor, asistente)'
    )
    corredor_numero = Column(
        Integer, 
        ForeignKey('corredores.numero', ondelete='SET NULL'), 
        nullable=True,
        index=True,
        comment='Referencia al corredor asociado (si aplica)'
    )
    comision_porcentaje = Column(
        Float, 
        default=0.0,
        comment='Porcentaje de comisión que recibe el corredor (si aplica)'
    )
    telefono = Column(
        String(20),
        nullable=True,
        comment='Número de teléfono de contacto del usuario'
    )
    fecha_creacion = Column(
        DateTime(timezone=True), 
        default=get_utc_now,
        nullable=False,
        comment='Fecha y hora de creación del registro'
    )
    fecha_modificacion = Column(
        DateTime(timezone=True), 
        default=get_utc_now, 
        onupdate=get_utc_now,
        nullable=False,
        comment='Fecha y hora de la última actualización del registro'
    )
    intentos_fallidos = Column(
        Integer, 
        default=0, 
        nullable=False,
        comment='Número de intentos fallidos de inicio de sesión consecutivos'
    )
    bloqueado_hasta = Column(
        DateTime(timezone=True), 
        nullable=True,
        comment='Fecha y hora hasta la que la cuenta está bloqueada (NULL si no está bloqueada)'
    )
    ultimo_intento_fallido = Column(
        DateTime(timezone=True), 
        nullable=True,
        comment='Fecha y hora del último intento fallido de inicio de sesión'
    )
    
    # Relaciones
    corredor_rel = relationship(
        'Corredor', 
        back_populates='usuarios',
        lazy='joined'
    )
    
    # Relaciones con clientes
    clientes_creados = relationship(
        'Cliente',
        foreign_keys='Cliente.creado_por_id',
        back_populates='creado_por_usuario',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    clientes_modificados = relationship(
        'Cliente',
        foreign_keys='Cliente.modificado_por_id',
        back_populates='modificado_por_usuario',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    # Índices adicionales
    __table_args__ = (
        # Índice compuesto para búsquedas por nombre y apellido
        {'sqlite_autoincrement': True},
    )

    # Métodos de instancia
    def __repr__(self) -> str:
        """Representación en cadena del objeto Usuario."""
        return f"<Usuario(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto Usuario a un diccionario.
        
        Returns:
            Dict[str, Any]: Diccionario con los atributos del usuario
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'username': self.username,
            'is_active': self.is_active,
            'is_superuser': self.is_superuser,
            'role': self.role,
            'corredor_numero': self.corredor_numero,
            'comision_porcentaje': self.comision_porcentaje,
            'telefono': self.telefono,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            'intentos_fallidos': self.intentos_fallidos,
            'bloqueado_hasta': self.bloqueado_hasta.isoformat() if self.bloqueado_hasta else None,
            'ultimo_intento_fallido': self.ultimo_intento_fallido.isoformat() if self.ultimo_intento_fallido else None
        }
    
    @classmethod
    def from_entity(cls: Type[T], entity: UsuarioEntity) -> T:
        """
        Crea una instancia de Usuario a partir de una entidad UsuarioEntity.
        
        Args:
            entity: Entidad de dominio UsuarioEntity
            
        Returns:
            Usuario: Instancia del modelo de base de datos
        """
        if not entity:
            raise ValueError("La entidad no puede ser nula")
            
        return cls(
            id=entity.id,
            nombre=entity.nombre,
            apellido=entity.apellido,
            email=entity.email,
            username=entity.username,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
            is_superuser=entity.is_superuser,
            role=entity.role.value if hasattr(entity.role, 'value') else entity.role,
            corredor_numero=entity.corredor_numero,
            comision_porcentaje=entity.comision_porcentaje,
            telefono=entity.telefono,
            intentos_fallidos=entity.intentos_fallidos or 0,
            bloqueado_hasta=entity.bloqueado_hasta,
            ultimo_intento_fallido=entity.ultimo_intento_fallido
        )
    
    def to_entity(self) -> UsuarioEntity:
        """
        Convierte el modelo de base de datos a una entidad de dominio.
        
        Returns:
            UsuarioEntity: Entidad de dominio UsuarioEntity
        """
        return UsuarioEntity(
            id=self.id,
            nombre=self.nombre,
            apellido=self.apellido,
            email=self.email,
            username=self.username,
            hashed_password=self.hashed_password,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            role=self.role,
            corredor_numero=self.corredor_numero,
            comision_porcentaje=self.comision_porcentaje,
            telefono=self.telefono,
            fecha_creacion=self.fecha_creacion,
            fecha_modificacion=self.fecha_modificacion,
            intentos_fallidos=self.intentos_fallidos or 0,
            bloqueado_hasta=self.bloqueado_hasta,
            ultimo_intento_fallido=self.ultimo_intento_fallido
        )
    
    # Métodos para el manejo de bloqueo de cuenta
    def registrar_intento_fallido(self) -> None:
        """
        Registra un intento fallido de inicio de sesión.
        
        Si se supera el número máximo de intentos, bloquea la cuenta.
        """
        ahora = get_utc_now()
        
        # Si ha pasado más de 1 hora desde el último intento, reiniciar el contador
        if (self.ultimo_intento_fallido and 
            (ahora - self.ultimo_intento_fallido).total_seconds() > 3600):
            self.intentos_fallidos = 0
        
        # Incrementar el contador de intentos fallidos
        self.intentos_fallidos = (self.intentos_fallidos or 0) + 1
        self.ultimo_intento_fallido = ahora
        
        # Bloquear la cuenta si se supera el límite de intentos
        if self.intentos_fallidos >= settings.MAX_LOGIN_ATTEMPTS:
            self.bloquear()
    
    def reiniciar_intentos_fallidos(self) -> None:
        """
        Reinicia el contador de intentos fallidos y desbloquea la cuenta.
        """
        self.intentos_fallidos = 0
        self.ultimo_intento_fallido = None
        self.bloqueado_hasta = None
    
    def bloquear(self, minutos: Optional[int] = None) -> None:
        """
        Bloquea la cuenta por el tiempo especificado.
        
        Args:
            minutos: Tiempo de bloqueo en minutos. Si es None, se usa el valor por defecto.
        """
        if minutos is None:
            minutos = settings.ACCOUNT_LOCKOUT_MINUTES
            
        self.bloqueado_hasta = get_utc_now() + timedelta(minutes=minutos)
    
    def desbloquear(self) -> None:
        """
        Desbloquea la cuenta y reinicia los contadores de intentos fallidos.
        """
        self.reiniciar_intentos_fallidos()
    
    def actualizar_ultimo_acceso(self) -> None:
        """
        Actualiza la fecha del último acceso exitoso.
        
        Nota: Este método está aquí por compatibilidad, pero en realidad
        la fecha de último acceso se maneja en el servicio de autenticación.
        """
        pass
    
    def tiene_permiso(self, permiso: str) -> bool:
        """
        Verifica si el usuario tiene un permiso específico.
        
        Args:
            permiso: Nombre del permiso a verificar
            
        Returns:
            bool: True si el usuario tiene el permiso, False en caso contrario
        """
        # Implementación básica - puede extenderse según los roles y permisos
        if self.is_superuser:
            return True
            
        # Aquí se puede implementar lógica más compleja de verificación de permisos
        return False
    
    def es_admin(self) -> bool:
        """
        Verifica si el usuario es administrador.
        
        Returns:
            bool: True si el usuario es administrador, False en caso contrario
        """
        return self.role == Role.ADMIN.value or self.is_superuser
    
    def es_corredor(self) -> bool:
        """
        Verifica si el usuario es un corredor.
        
        Returns:
            bool: True si el usuario es corredor, False en caso contrario
        """
        return self.role == Role.CORREDOR.value
    
    def es_asistente(self) -> bool:
        """
        Verifica si el usuario es un asistente.
        
        Returns:
            bool: True si el usuario es asistente, False en caso contrario
        """
        return self.role == Role.ASISTENTE.value


# Eventos de SQLAlchemy
@event.listens_for(Usuario, 'before_insert')
def set_timestamps_before_insert(mapper, connection, target):
    """
    Establece las marcas de tiempo antes de insertar un nuevo usuario.
    
    Args:
        mapper: Mapper que está siendo usado
        connection: Conexión a la base de datos
        target: Instancia del modelo Usuario que se está insertando
    """
    ahora = get_utc_now()
    if not target.fecha_creacion:
        target.fecha_creacion = ahora
    if not target.fecha_modificacion:
        target.fecha_modificacion = ahora


@event.listens_for(Usuario, 'before_update')
def set_timestamp_before_update(mapper, connection, target):
    """
    Actualiza la marca de tiempo antes de actualizar un usuario.
    
    Args:
        mapper: Mapper que está siendo usado
        connection: Conexión a la base de datos
        target: Instancia del modelo Usuario que se está actualizando
    """
    target.fecha_modificacion = get_utc_now()
