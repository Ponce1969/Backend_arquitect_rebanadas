from typing import List, Optional

from .dtos import (
    RegistroUsuarioCommand,
    ActualizarUsuarioCommand,
    CambiarContrasenaCommand,
    LoginCommand,
    UsuarioDto,
    TokenDto
)
from .interfaces.repositories import AbstractUsuarioRepository
from ..domain.entities import Usuario
from domain.shared.types import Role

# Importamos la utilidad de hashing de contraseñas
from infrastructure.security.password import PasswordHelper


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
    """Caso de uso para obtener un usuario por su ID."""

    def __init__(self, repository: AbstractUsuarioRepository):
        self.repository = repository

    def execute(self, usuario_id: int) -> Optional[UsuarioDto]:
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            return None

        return UsuarioDto(
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


class ListarUsuariosUseCase:
    """Caso de uso para listar todos los usuarios."""

    def __init__(self, repository: AbstractUsuarioRepository):
        self.repository = repository

    def execute(self) -> List[UsuarioDto]:
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

    def execute(self, corredor_numero: int) -> List[UsuarioDto]:
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

    def execute(self, usuario_id: int, command: ActualizarUsuarioCommand) -> Optional[UsuarioDto]:
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
    """Caso de uso para autenticar un usuario."""

    def __init__(self, repository: AbstractUsuarioRepository, password_helper: PasswordHelper):
        self.repository = repository
        self.password_helper = password_helper

    def execute(self, command: LoginCommand) -> Optional[UsuarioDto]:
        # Obtener usuario por username
        usuario = self.repository.get_by_username(command.username)
        if not usuario or not usuario.is_active:
            return None

        # Obtener la contraseña hasheada
        hashed_password = self.repository.get_hashed_password(usuario.id)
        if not hashed_password:
            return None

        # Verificar la contraseña
        if not self.password_helper.verify_password(command.password, hashed_password):
            return None

        # Retornar DTO del usuario autenticado
        return UsuarioDto(
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
