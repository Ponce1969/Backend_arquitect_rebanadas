import abc
from datetime import datetime
from typing import List, Optional

# Importamos la Entidad de Dominio Usuario
from features.usuarios.domain.entities import Usuario as UsuarioEntity


class AbstractUsuarioRepository(abc.ABC):
    """Interfaz Abstracta para el Repositorio de Usuarios."""

    @abc.abstractmethod
    def add(self, usuario: UsuarioEntity, hashed_password: str) -> UsuarioEntity:
        """Añade un nuevo usuario al repositorio con su contraseña hasheada."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, usuario_id: int) -> Optional[UsuarioEntity]:
        """Obtiene un usuario por su ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_username(self, username: str) -> Optional[UsuarioEntity]:
        """Obtiene un usuario por su nombre de usuario."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str) -> Optional[UsuarioEntity]:
        """Obtiene un usuario por su correo electrónico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[UsuarioEntity]:
        """Obtiene todos los usuarios."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, usuario: UsuarioEntity) -> UsuarioEntity:
        """Actualiza un usuario existente."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, usuario_id: int) -> bool:
        """Elimina un usuario por su ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_usuarios_by_corredor(self, corredor_numero: int) -> List[UsuarioEntity]:
        """Obtiene usuarios asociados a un corredor específico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_hashed_password(self, usuario_id: int) -> Optional[str]:
        """Obtiene la contraseña hasheada de un usuario por su ID."""
        raise NotImplementedError
        
    @abc.abstractmethod
    def update_password(self, usuario_id: int, hashed_password: str) -> None:
        """Actualiza la contraseña hasheada de un usuario."""
        raise NotImplementedError

    @abc.abstractmethod
    def registrar_intento_fallido(self, usuario_id: int) -> None:
        """Registra un intento fallido de inicio de sesión."""
        raise NotImplementedError
        
    @abc.abstractmethod
    def reiniciar_intentos_fallidos(self, usuario_id: int) -> None:
        """Reinicia el contador de intentos fallidos de un usuario."""
        raise NotImplementedError
        
    @abc.abstractmethod
    def bloquear_usuario(self, usuario_id: int, hasta: datetime) -> None:
        """Bloquea un usuario hasta la fecha especificada."""
        raise NotImplementedError
        
    @abc.abstractmethod
    def desbloquear_usuario(self, usuario_id: int) -> None:
        """Desbloquea un usuario."""
        raise NotImplementedError
