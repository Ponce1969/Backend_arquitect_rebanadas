import abc
from typing import List, Optional

# Importamos la Entidad de Dominio Usuario
from features.usuarios.domain.entities import Usuario


class AbstractUsuarioRepository(abc.ABC):
    """Interfaz Abstracta para el Repositorio de Usuarios."""

    @abc.abstractmethod
    def add(self, usuario: Usuario, hashed_password: str) -> Usuario:
        """Añade un nuevo usuario al repositorio con su contraseña hasheada."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_username(self, username: str) -> Optional[Usuario]:
        """Obtiene un usuario por su nombre de usuario."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por su correo electrónico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[Usuario]:
        """Obtiene todos los usuarios."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario existente."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, usuario_id: int) -> bool:
        """Elimina un usuario por su ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_usuarios_by_corredor(self, corredor_numero: int) -> List[Usuario]:
        """Obtiene usuarios asociados a un corredor específico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_hashed_password(self, usuario_id: int) -> Optional[str]:
        """Obtiene la contraseña hasheada de un usuario por su ID."""
        raise NotImplementedError
        
    @abc.abstractmethod
    def update_password(self, usuario_id: int, hashed_password: str) -> bool:
        """Actualiza la contraseña hasheada de un usuario."""
        raise NotImplementedError
