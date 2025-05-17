from dataclasses import dataclass
from datetime import datetime

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
    # La contraseña hashed no está en la Entidad de Dominio por seguridad
    is_active: bool = True
    is_superuser: bool = False
    role: Role = Role.CORREDOR  # Usamos el Enum Role del dominio compartido
    # Referencia al número del Corredor (si existe la asociación)
    corredor_numero: int | None = None  # Puede ser None para admins/asistentes
    comision_porcentaje: float = 0.0
    telefono: str | None = None
    fecha_creacion: datetime | None = None
    fecha_modificacion: datetime | None = None

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
    def activate(self):
        """Activa el usuario."""
        self.is_active = True

    def deactivate(self):
        """Desactiva el usuario."""
        self.is_active = False

    def assign_role(self, new_role: Role):
        """Asigna un nuevo rol al usuario."""
        self.role = new_role
        # Validar consistencia después del cambio de rol
        if not self.validate_role_consistency():
            raise ValueError(f"Inconsistencia de rol: un usuario con rol {new_role} debe tener una asociación de corredor.")
