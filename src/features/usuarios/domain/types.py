import enum


# Enum para los roles de usuario
class Role(str, enum.Enum):
    ADMIN = "admin"
    CORREDOR = "corredor"
    ASISTENTE = "asistente"
    # Otros roles si aplican

# Diccionario para definir permisos por rol
# Esto es un ejemplo simple. En un sistema real, podría ser más complejo.
class RolePermissions:
    _permissions: dict[Role, set[str]] = {
        Role.ADMIN: {
            "aseguradoras:read", "aseguradoras:write",
            "clientes:read", "clientes:write", "clientes:view_all",
            "corredores:read", "corredores:write",
            "polizas:read", "polizas:write",
            "tipos_seguros:read", "tipos_seguros:write",
            "usuarios:read", "usuarios:write", "usuarios:manage_roles", "usuarios:manage_superusers",
        },
        Role.CORREDOR: {
            "aseguradoras:read",
            "clientes:read", "clientes:write",
            "polizas:read", "polizas:write",
            "tipos_seguros:read",
        },
        Role.ASISTENTE: {
            "aseguradoras:read",
            "clientes:read",
            "polizas:read",
            "tipos_seguros:read",
        }
    }
    
    @classmethod
    def get_permissions(cls, role: Role) -> set[str]:
        """Obtiene los permisos para un rol específico."""
        return cls._permissions.get(role, set())
    
    @classmethod
    def has_permission(cls, role: Role, permission: str) -> bool:
        """Verifica si un rol tiene un permiso específico."""
        return permission in cls.get_permissions(role)
