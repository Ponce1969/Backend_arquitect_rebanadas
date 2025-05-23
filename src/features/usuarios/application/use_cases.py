

# Importamos la utilidad de hashing de contraseñas
from typing import Optional, Tuple

from src.infrastructure.security.password import Argon2PasswordHelper as PasswordHelper

from ..domain.entities import Usuario
from ..domain.services.autenticacion_service import AutenticacionService
from .dtos import (
    ActualizarUsuarioCommand,
    CambiarContrasenaCommand,
    LoginCommand,
    RegistroUsuarioCommand,
    UsuarioDto,
)
from .interfaces.repositories import AbstractUsuarioRepository


class RegistrarUsuarioUseCase:
    """Caso de uso para registrar un nuevo usuario."""

    def __init__(self, repository: AbstractUsuarioRepository, password_helper: PasswordHelper):
        self.repository = repository
        self.password_helper = password_helper

    def execute(self, command: RegistroUsuarioCommand) -> UsuarioDto:
        # Verificar si el username ya existe
        existing_user = self.repository.get_by_username(command.username)
        if existing_user:
            raise ValueError(f"El nombre de usuario '{command.username}' ya existe.")

        # Verificar si el email ya existe
        existing_email = self.repository.get_by_email(command.email)
        if existing_email:
            raise ValueError(f"El correo electrónico '{command.email}' ya existe.")

        # Hashear la contraseña
        hashed_password = self.password_helper.hash_password(command.password)

        # Crear entidad de dominio
        usuario = Usuario(
            nombre=command.nombre,
            apellido=command.apellido,
            email=command.email,
            username=command.username,
            is_active=command.is_active,
            is_superuser=command.is_superuser,
            role=command.role,
            corredor_numero=command.corredor_numero,
            comision_porcentaje=command.comision_porcentaje,
            telefono=command.telefono,
        )

        # Validar consistencia de rol
        if not usuario.validate_role_consistency():
            raise ValueError("El rol asignado no es consistente con los datos proporcionados.")

        # Persistir la entidad con la contraseña hasheada
        created_usuario = self.repository.add(usuario, hashed_password)

        # Retornar DTO
        return UsuarioDto(
            id=created_usuario.id,
            nombre=created_usuario.nombre,
            apellido=created_usuario.apellido,
            email=created_usuario.email,
            username=created_usuario.username,
            is_active=created_usuario.is_active,
            is_superuser=created_usuario.is_superuser,
            role=created_usuario.role,
            corredor_numero=created_usuario.corredor_numero,
            comision_porcentaje=created_usuario.comision_porcentaje,
            telefono=created_usuario.telefono,
            fecha_creacion=created_usuario.fecha_creacion,
            fecha_modificacion=created_usuario.fecha_modificacion,
        )


class ObtenerUsuarioUseCase:
    """
    Caso de uso para obtener un usuario.
    
    Este caso de uso puede obtener un usuario por su ID o por su nombre de usuario.
    """

    def __init__(self, repository: AbstractUsuarioRepository):
        self.repository = repository

    def execute(self, usuario_id: int = None, username: str = None) -> Usuario | None:
        """
        Obtiene un usuario por su ID o por su nombre de usuario.
        
        Args:
            usuario_id: ID del usuario a buscar (opcional)
            username: Nombre de usuario a buscar (opcional)
            
        Returns:
            Usuario: La entidad de usuario si se encuentra, None en caso contrario
            
        Nota:
            Si se proporcionan tanto usuario_id como username, se prioriza el ID.
        """
        if usuario_id is not None:
            return self.repository.get_by_id(usuario_id)
        elif username is not None:
            return self.repository.get_by_username(username)
        return None


class ListarUsuariosUseCase:
    """Caso de uso para listar todos los usuarios."""

    def __init__(self, repository: AbstractUsuarioRepository):
        self.repository = repository

    def execute(self) -> list[UsuarioDto]:
        usuarios = self.repository.get_all()
        return [
            UsuarioDto(
                id=usuario.id,
                nombre=usuario.nombre,
                apellido=usuario.apellido,
                email=usuario.email,
                username=usuario.username,
                is_active=usuario.is_active,
                is_superuser=usuario.is_superuser,
                role=usuario.role,
                corredor_numero=usuario.corredor_numero,
                comision_porcentaje=usuario.comision_porcentaje,
                telefono=usuario.telefono,
                fecha_creacion=usuario.fecha_creacion,
                fecha_modificacion=usuario.fecha_modificacion,
            )
            for usuario in usuarios
        ]


class ListarUsuariosPorCorredorUseCase:
    """Caso de uso para listar usuarios asociados a un corredor."""

    def __init__(self, repository: AbstractUsuarioRepository):
        self.repository = repository

    def execute(self, corredor_numero: int) -> list[UsuarioDto]:
        usuarios = self.repository.get_usuarios_by_corredor(corredor_numero)
        return [
            UsuarioDto(
                id=usuario.id,
                nombre=usuario.nombre,
                apellido=usuario.apellido,
                email=usuario.email,
                username=usuario.username,
                is_active=usuario.is_active,
                is_superuser=usuario.is_superuser,
                role=usuario.role,
                corredor_numero=usuario.corredor_numero,
                comision_porcentaje=usuario.comision_porcentaje,
                telefono=usuario.telefono,
                fecha_creacion=usuario.fecha_creacion,
                fecha_modificacion=usuario.fecha_modificacion,
            )
            for usuario in usuarios
        ]


class ActualizarUsuarioUseCase:
    """Caso de uso para actualizar un usuario existente."""

    def __init__(self, repository: AbstractUsuarioRepository):
        self.repository = repository

    def execute(self, usuario_id: int, command: ActualizarUsuarioCommand) -> UsuarioDto | None:
        # Verificar si el usuario existe
        existing_usuario = self.repository.get_by_id(usuario_id)
        if not existing_usuario:
            return None

        # Verificar si el nuevo username ya está en uso por otro usuario
        if command.username and command.username != existing_usuario.username:
            existing = self.repository.get_by_username(command.username)
            if existing and existing.id != usuario_id:
                raise ValueError(f"El nombre de usuario '{command.username}' ya está en uso.")

        # Verificar si el nuevo email ya está en uso por otro usuario
        if command.email and command.email != existing_usuario.email:
            existing = self.repository.get_by_email(command.email)
            if existing and existing.id != usuario_id:
                raise ValueError(f"El correo electrónico '{command.email}' ya está en uso.")

        # Actualizar los campos de la entidad existente
        updated_usuario = Usuario(
            id=existing_usuario.id,
            nombre=command.nombre if command.nombre is not None else existing_usuario.nombre,
            apellido=command.apellido if command.apellido is not None else existing_usuario.apellido,
            email=command.email if command.email is not None else existing_usuario.email,
            username=command.username if command.username is not None else existing_usuario.username,
            is_active=command.is_active if command.is_active is not None else existing_usuario.is_active,
            is_superuser=command.is_superuser if command.is_superuser is not None else existing_usuario.is_superuser,
            role=command.role if command.role is not None else existing_usuario.role,
            corredor_numero=command.corredor_numero if command.corredor_numero is not None else existing_usuario.corredor_numero,
            comision_porcentaje=command.comision_porcentaje if command.comision_porcentaje is not None else existing_usuario.comision_porcentaje,
            telefono=command.telefono if command.telefono is not None else existing_usuario.telefono,
            fecha_creacion=existing_usuario.fecha_creacion,
            fecha_modificacion=existing_usuario.fecha_modificacion,
        )

        # Validar consistencia de rol
        if not updated_usuario.validate_role_consistency():
            raise ValueError("El rol asignado no es consistente con los datos proporcionados.")

        # Actualizar en el repositorio
        updated = self.repository.update(updated_usuario)

        # Retornar DTO
        return UsuarioDto(
            id=updated.id,
            nombre=updated.nombre,
            apellido=updated.apellido,
            email=updated.email,
            username=updated.username,
            is_active=updated.is_active,
            is_superuser=updated.is_superuser,
            role=updated.role,
            corredor_numero=updated.corredor_numero,
            comision_porcentaje=updated.comision_porcentaje,
            telefono=updated.telefono,
            fecha_creacion=updated.fecha_creacion,
            fecha_modificacion=updated.fecha_modificacion,
        )


class CambiarContrasenaUseCase:
    """Caso de uso para cambiar la contraseña de un usuario."""

    def __init__(self, repository: AbstractUsuarioRepository, password_helper: PasswordHelper):
        self.repository = repository
        self.password_helper = password_helper

    def execute(self, command: CambiarContrasenaCommand) -> bool:
        # Verificar si el usuario existe
        usuario = self.repository.get_by_id(command.usuario_id)
        if not usuario:
            raise ValueError(f"Usuario con ID {command.usuario_id} no encontrado.")

        # Obtener la contraseña hasheada actual
        hashed_password = self.repository.get_hashed_password(command.usuario_id)
        if not hashed_password:
            raise ValueError("No se pudo obtener la contraseña actual.")

        # Verificar la contraseña actual
        if not self.password_helper.verify_password(command.contrasena_actual, hashed_password):
            raise ValueError("La contraseña actual es incorrecta.")

        # Hashear la nueva contraseña
        new_hashed_password = self.password_helper.hash_password(command.nueva_contrasena)

        # Actualizar la contraseña en el repositorio
        result = self.repository.update_password(command.usuario_id, new_hashed_password)
        if not result:
            raise ValueError(f"No se pudo actualizar la contraseña del usuario {command.usuario_id}.")

        return True


class EliminarUsuarioUseCase:
    """Caso de uso para eliminar un usuario."""

    def __init__(self, repository: AbstractUsuarioRepository):
        self.repository = repository

    def execute(self, usuario_id: int) -> bool:
        return self.repository.delete(usuario_id)


class AutenticarUsuarioUseCase:
    """
    Caso de uso para autenticar un usuario en el sistema.
    
    Este caso de uso maneja la lógica de autenticación de usuarios, incluyendo:
    - Validación de credenciales
    - Manejo de bloqueos por intentos fallidos
    - Generación de tokens de acceso
    """

    def __init__(
        self, 
        usuario_repository: AbstractUsuarioRepository, 
        autenticacion_service: AutenticacionService
    ):
        """
        Inicializa el caso de uso con las dependencias necesarias.
        
        Args:
            usuario_repository: Repositorio para acceder a los datos de usuarios
            autenticacion_service: Servicio de autenticación
        """
        self.usuario_repository = usuario_repository
        self.autenticacion_service = autenticacion_service

    def execute(self, command: LoginCommand) -> Tuple[Optional[UsuarioDto], Optional[str]]:
        """
        Autentica a un usuario con su nombre de usuario y contraseña.
        
        Este método es el punto de entrada principal para el proceso de autenticación.
        Maneja la lógica de autenticación y devuelve un DTO del usuario autenticado
        o un mensaje de error en caso de fallo.
        
        Args:
            command: Comando con las credenciales de autenticación
            
        Returns:
            Tuple[Optional[UsuarioDto], Optional[str]]: 
                - DTO del usuario autenticado si las credenciales son válidas, None en caso contrario
                - Mensaje de error si la autenticación falla, None si es exitosa
                
        Example:
            >>> use_case = AutenticarUsuarioUseCase(repo, auth_service)
            >>> usuario_dto, error = use_case.execute(LoginCommand(username="user", password="pass"))
            >>> if usuario_dto:
            ...     print(f"Bienvenido {usuario_dto.nombre}")
            ... else:
            ...     print(f"Error: {error}")
        """
        try:
            # Validar que el comando no sea None
            if not command or not command.username or not command.password:
                return None, "Se requieren nombre de usuario y contraseña"
            
            # Autenticar al usuario usando el servicio de autenticación
            usuario, error = self.autenticacion_service.autenticar_usuario(
                command.username, command.password
            )
            
            # Si hay un error o el usuario no existe, devolver el mensaje de error
            if error or not usuario:
                return None, error or "Credenciales inválidas"
                
            # Verificar si la cuenta está activa
            if not usuario.is_active:
                return None, "La cuenta del usuario está desactivada"

            # Convertir la entidad de dominio a DTO para la capa de presentación
            usuario_dto = UsuarioDto(
                id=usuario.id,
                nombre=usuario.nombre,
                apellido=usuario.apellido,
                email=usuario.email,
                username=usuario.username,
                is_active=usuario.is_active,
                is_superuser=usuario.is_superuser,
                role=usuario.role,
                corredor_numero=usuario.corredor_numero,
                comision_porcentaje=usuario.comision_porcentaje,
                telefono=usuario.telefono,
                fecha_creacion=usuario.fecha_creacion,
                fecha_modificacion=usuario.fecha_modificacion,
            )
            
            return usuario_dto, None
            
        except Exception as e:
            # Registrar el error para diagnóstico
            print(f"Error en AutenticarUsuarioUseCase: {str(e)}")
            return None, "Ocurrió un error al procesar la autenticación"
