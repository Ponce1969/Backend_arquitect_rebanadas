from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

# Importamos los tipos compartidos (Roles y Permisos)
from src.features.usuarios.domain.types import Role, RolePermissions


@dataclass
class Usuario:
    """Entidad de Dominio para un Usuario."""
    id: int | None = None  # ID es Integer y generado por DB
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    username: str = ""
    hashed_password: str = ""  # Campo para la contraseña hasheada
    is_active: bool = True
    is_superuser: bool = False
    role: Role = Role.CORREDOR  # Usamos el Enum Role del dominio compartido
    # Referencia al número del Corredor (si existe la asociación)
    corredor_numero: int | None = None  # Puede ser None para admins/asistentes
    comision_porcentaje: float = 0.0
    telefono: str | None = None
    fecha_creacion: datetime | None = None
    fecha_modificacion: datetime | None = None
    
    # Campos para el bloqueo de cuenta
    intentos_fallidos: int = 0
    bloqueado_hasta: Optional[datetime] = None
    ultimo_intento_fallido: Optional[datetime] = None

    # Lógica de Dominio
    def has_permission(self, permission: str) -> bool:
        """Verifica si el usuario tiene un permiso específico basado en su rol y estado."""
        if self.is_superuser:
            return True  # Los superusuarios tienen todos los permisos

        if not self.is_active:
            return False  # Los usuarios inactivos no tienen permisos

        # Usar la lógica de permisos definida en los tipos compartidos
        return RolePermissions.has_permission(self.role, permission)

    def validate_role_consistency(self) -> bool:
        """Valida que el rol del usuario sea consistente con sus atributos."""
        # Si el rol es corredor, debe tener un corredor asociado
        if self.role == Role.CORREDOR and self.corredor_numero is None:
            return False

        return True

    # Métodos de negocio relacionados con un Usuario
    def is_active(self) -> bool:
        """
        Verifica si el usuario está activo y no bloqueado.
        
        Returns:
            bool: True si el usuario está activo y no bloqueado, False en caso contrario.
        """
        if not self.is_active:
            return False
            
        # Verificar si el usuario está bloqueado temporalmente
        if self.bloqueado_hasta and self.bloqueado_hasta > datetime.now():
            return False
            
        # Si el tiempo de bloqueo ha expirado, reiniciar el contador
        if self.bloqueado_hasta and self.bloqueado_hasta <= datetime.now():
            self.bloqueado_hasta = None
            self.intentos_fallidos = 0
            
        return True
        
    def esta_bloqueado(self) -> bool:
        """
        Verifica si la cuenta del usuario está actualmente bloqueada.
        
        Returns:
            bool: True si la cuenta está bloqueada, False en caso contrario.
        """
        if not self.bloqueado_hasta:
            return False
            
        # Si el tiempo de bloqueo ha expirado, desbloquear la cuenta
        if self.bloqueado_hasta <= datetime.now():
            self.bloqueado_hasta = None
            self.intentos_fallidos = 0
            return False
            
        return True
        
    def obtener_tiempo_restante_bloqueo(self) -> Optional[int]:
        """
        Obtiene el tiempo restante de bloqueo en segundos.
        
        Returns:
            Optional[int]: Tiempo restante en segundos, o None si no está bloqueado.
        """
        if not self.esta_bloqueado():
            return None
            
        return int((self.bloqueado_hasta - datetime.now()).total_seconds())

    def activate(self):
        """Activa el usuario."""
        self.is_active = True

    def deactivate(self):
        """
        Desactiva el usuario y reinicia los intentos fallidos.
        """
        self.is_active = False
        self.intentos_fallidos = 0
        self.bloqueado_hasta = None
        self.ultimo_intento_fallido = None

    def assign_role(self, new_role: Role):
        """Asigna un nuevo rol al usuario."""
        self.role = new_role
        # Validar consistencia después del cambio de rol
        if not self.validate_role_consistency():
            raise ValueError(f"Inconsistencia de rol: un usuario con rol {new_role} debe tener una asociación de corredor.")
