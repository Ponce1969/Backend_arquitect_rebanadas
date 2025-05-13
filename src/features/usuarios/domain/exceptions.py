class UsuarioException(Exception):
    """Excepción base para el slice de Usuarios."""
    pass


class UsuarioNotFoundException(UsuarioException):
    """Excepción lanzada cuando no se encuentra un usuario."""
    def __init__(self, usuario_id: int):
        self.usuario_id = usuario_id
        self.message = f"No se encontró el usuario con ID {usuario_id}"
        super().__init__(self.message)


class UsuarioUsernameExistsException(UsuarioException):
    """Excepción lanzada cuando ya existe un usuario con el mismo nombre de usuario."""
    def __init__(self, username: str):
        self.username = username
        self.message = f"Ya existe un usuario con el nombre de usuario {username}"
        super().__init__(self.message)


class UsuarioEmailExistsException(UsuarioException):
    """Excepción lanzada cuando ya existe un usuario con el mismo email."""
    def __init__(self, email: str):
        self.email = email
        self.message = f"Ya existe un usuario con el email {email}"
        super().__init__(self.message)


class UsuarioCredencialesInvalidasException(UsuarioException):
    """Excepción lanzada cuando las credenciales de un usuario son inválidas."""
    def __init__(self):
        self.message = "Credenciales inválidas"
        super().__init__(self.message)


class UsuarioInactivoException(UsuarioException):
    """Excepción lanzada cuando se intenta acceder con un usuario inactivo."""
    def __init__(self, username: str):
        self.username = username
        self.message = f"El usuario {username} está inactivo"
        super().__init__(self.message)


class UsuarioContrasenaInvalidaException(UsuarioException):
    """Excepción lanzada cuando la contraseña actual no coincide."""
    def __init__(self):
        self.message = "La contraseña actual no es correcta"
        super().__init__(self.message)
