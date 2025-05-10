import enum
from typing import Set, Dict

# Enum para los roles de usuario
class Role(str, enum.Enum):
    ADMIN = "admin"
    CORREDOR = "corredor"
    ASISTENTE = "asistente"
    # Otros roles si aplican

# Diccionario para definir permisos por rol
# Esto es un ejemplo simple. En un sistema real, podría ser más complejo.
class RolePermissions:
    _permissions: Dict[Role, Set[str]] = {
        Role.ADMIN: {
            "aseguradoras:read", "aseguradoras:write",
            "clientes:read", "clientes:write", "clientes:view_all",
            "corredores:read", "corredores:write",
            "polizas:read", "polizas:write",
            "tipos_seguros:read", "tipos_seguros:write",
            "usuarios:read", "usuarios:write", "usuarios:manage_roles", "usuarios:manage_superusers",
        },
        Role.CORREDOR: {
            "clientes:read", "clientes:write", "clientes:view_own", # Permiso específico para ver solo los suyos
            "polizas:read", "polizas:write",
            "tipos_seguros:read", # Un corredor solo ve tipos de seguro, no los gestiona
            "usuarios:read_own_profile", # Puede ver su propio perfil
        },
        Role.ASISTENTE: {
            "clientes:read", "clientes:write", "clientes:view_all", # Un asistente puede ver todos los clientes
            "polizas:read", "polizas:write",
            "tipos_seguros:read",
            "usuarios:read_own_profile",
        }
        # Añadir permisos para otros roles
    }

    @staticmethod
    def get_permissions(role: Role) -> Set[str]:
        """Obtiene el conjunto de permisos para un rol dado."""
        return RolePermissions._permissions.get(role, set())

    @staticmethod
    def has_permission(role: Role, permission: str) -> bool:
        """Verifica si un rol tiene un permiso específico."""
        return permission in RolePermissions.get_permissions(role)
