
"""
Implementación del repositorio de usuarios usando SQLAlchemy.

Este módulo proporciona una implementación concreta del repositorio abstracto de usuarios
utilizando SQLAlchemy como ORM para interactuar con la base de datos.
"""
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.features.usuarios.application.interfaces.repositories import AbstractUsuarioRepository
from src.features.usuarios.domain.entities import Usuario as UsuarioEntity
from .models import Usuario as UsuarioModel


class SQLAlchemyUsuarioRepository(AbstractUsuarioRepository):
    """
    Implementación del Repositorio de Usuarios usando SQLAlchemy.
    
    Esta clase proporciona una implementación concreta del repositorio abstracto
    de usuarios, utilizando SQLAlchemy para interactuar con la base de datos.
    """

    def __init__(self, session: Session):
        """
        Inicializa el repositorio con una sesión de SQLAlchemy.
        
        Args:
            session: Sesión de SQLAlchemy para interactuar con la base de datos
        """
        self.session = session
        
    def _get_utc_now(self) -> datetime:
        """
        Obtiene la fecha y hora actual en UTC.
        
        Returns:
            datetime: Fecha y hora actual en zona horaria UTC
        """
        return datetime.now(timezone.utc)

    def _get_base_query(self):
        """
        Crea y retorna una consulta base con las relaciones cargadas de forma temprana.
        
        Returns:
            Query: Consulta base de SQLAlchemy con las relaciones cargadas
        """
        return self.session.query(UsuarioModel).options(
            # Carga temprana de la relación con Corredor si existe
            joinedload(UsuarioModel.corredor_rel)
        )
        
    def _to_entity(self, model: UsuarioModel) -> Optional[UsuarioEntity]:
        """
        Convierte un modelo de SQLAlchemy a una entidad de dominio.
        
        Args:
            model: Instancia del modelo SQLAlchemy a convertir
            
        Returns:
            Optional[UsuarioEntity]: Entidad de dominio o None si el modelo es None
        """
        if not model:
            return None
            
        return UsuarioEntity(
            id=model.id,
            nombre=model.nombre,
            apellido=model.apellido,
            email=model.email,
            username=model.username,
            hashed_password=model.hashed_password,  # Usamos el nombre del campo real
            is_active=model.is_active,
            is_superuser=model.is_superuser,
            role=model.role,
            corredor_numero=model.corredor_numero,
            comision_porcentaje=model.comision_porcentaje,
            telefono=model.telefono,
            fecha_creacion=model.fecha_creacion,
            fecha_modificacion=model.fecha_modificacion,
            intentos_fallidos=model.intentos_fallidos or 0,
            bloqueado_hasta=model.bloqueado_hasta,
            ultimo_intento_fallido=model.ultimo_intento_fallido,
        )

    def add(self, usuario: UsuarioEntity) -> UsuarioEntity:
        """
        Añade un nuevo usuario a la base de datos.
        
        Args:
            usuario: Entidad de usuario a guardar
            
        Returns:
            UsuarioEntity: Entidad de usuario con el ID asignado
            
        Raises:
            ValueError: Si ya existe un usuario con el mismo username o email
            Exception: Si ocurre un error al guardar el usuario
        """
        try:
            # Verificar si ya existe un usuario con el mismo username o email
            existing_username = self.get_by_username(usuario.username)
            if existing_username:
                raise ValueError(f"El nombre de usuario '{usuario.username}' ya está en uso.")

            existing_email = self.get_by_email(usuario.email)
            if existing_email:
                raise ValueError(f"El correo electrónico '{usuario.email}' ya está en uso.")

            # Convertir la entidad a modelo y guardar
            db_usuario = UsuarioModel.from_entity(usuario)
            self.session.add(db_usuario)
            self.session.flush()  # Para obtener el ID generado
            
            # Actualizar el ID en la entidad
            usuario.id = db_usuario.id
            
            return usuario
            
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Error de integridad al crear usuario: {e}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Error de base de datos al crear usuario: {e}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error inesperado al crear usuario: {e}")

    def get_by_id(self, usuario_id: int) -> Optional[UsuarioEntity]:
        """
        Obtiene un usuario por su ID.
        
        Args:
            usuario_id: ID del usuario a buscar
            
        Returns:
            Optional[UsuarioEntity]: Entidad de usuario si se encuentra, None en caso contrario
        """
        if not usuario_id:
            return None
            
        try:
            db_usuario = self._get_base_query().filter(UsuarioModel.id == usuario_id).first()
            return self._to_entity(db_usuario)
        except SQLAlchemyError as e:
            raise Exception(f"Error al buscar usuario por ID: {e}")

    def get_by_username(self, username: str) -> Optional[UsuarioEntity]:
        """
        Obtiene un usuario por su nombre de usuario (case-insensitive).
        
        Args:
            username: Nombre de usuario a buscar
            
        Returns:
            Optional[UsuarioEntity]: Entidad de usuario si se encuentra, None en caso contrario
        """
        if not username:
            return None
            
        try:
            db_usuario = (
                self._get_base_query()
                .filter(UsuarioModel.username.ilike(username))
                .first()
            )
            return self._to_entity(db_usuario)
        except SQLAlchemyError as e:
            raise Exception(f"Error al buscar usuario por nombre de usuario: {e}")

    def get_by_email(self, email: str) -> Optional[UsuarioEntity]:
        """
        Obtiene un usuario por su dirección de correo electrónico (case-insensitive).
        
        Args:
            email: Dirección de correo electrónico a buscar
            
        Returns:
            Optional[UsuarioEntity]: Entidad de usuario si se encuentra, None en caso contrario
        """
        if not email:
            return None
            
        try:
            db_usuario = (
                self._get_base_query()
                .filter(UsuarioModel.email.ilike(email))
                .first()
            )
            return self._to_entity(db_usuario)
        except SQLAlchemyError as e:
            raise Exception(f"Error al buscar usuario por correo electrónico: {e}")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[UsuarioEntity]:
        """
        Obtiene una lista paginada de todos los usuarios.
        
        Args:
            skip: Número de registros a omitir (para paginación)
            limit: Número máximo de registros a devolver
            
        Returns:
            List[UsuarioEntity]: Lista de entidades de usuario
        """
        try:
            db_usuarios = self._get_base_query().offset(skip).limit(limit).all()
            return [self._to_entity(u) for u in db_usuarios if u is not None]
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener la lista de usuarios: {e}")

    def update(self, usuario: UsuarioEntity) -> Optional[UsuarioEntity]:
        """
        Actualiza un usuario existente en la base de datos.
        
        Args:
            usuario: Entidad de usuario con los datos actualizados
            
        Returns:
            Optional[UsuarioEntity]: Entidad de usuario actualizada o None si no se encontró
            
        Raises:
            ValueError: Si el usuario no existe o hay conflictos de unicidad
            Exception: Si ocurre un error durante la actualización
        """
        if not usuario.id:
            raise ValueError("No se puede actualizar un usuario sin ID")
            
        try:
            db_usuario = self.session.get(UsuarioModel, usuario.id)
            if not db_usuario:
                raise ValueError(f"Usuario con ID {usuario.id} no encontrado.")

            # Verificar unicidad de username
            if usuario.username != db_usuario.username:
                existing = self.session.query(UsuarioModel).filter(
                    UsuarioModel.username.ilike(usuario.username),
                    UsuarioModel.id != usuario.id
                ).first()
                if existing:
                    raise ValueError(f"El nombre de usuario '{usuario.username}' ya está en uso.")

            # Verificar unicidad de email
            if usuario.email != db_usuario.email:
                existing = self.session.query(UsuarioModel).filter(
                    UsuarioModel.email.ilike(usuario.email),
                    UsuarioModel.id != usuario.id
                ).first()
                if existing:
                    raise ValueError(f"El correo electrónico '{usuario.email}' ya está en uso.")

            # Actualizar campos del modelo
            db_usuario.nombre = usuario.nombre
            db_usuario.apellido = usuario.apellido
            db_usuario.email = usuario.email
            db_usuario.username = usuario.username
            db_usuario.is_active = usuario.is_active
            db_usuario.is_superuser = usuario.is_superuser
            db_usuario.role = usuario.role
            db_usuario.corredor_numero = usuario.corredor_numero
            db_usuario.comision_porcentaje = usuario.comision_porcentaje
            db_usuario.telefono = usuario.telefono
            
            # Actualizar fechas
            ahora = self._get_utc_now()
            db_usuario.fecha_modificacion = ahora
            
            # Actualizar campos de bloqueo si es necesario
            if hasattr(usuario, 'intentos_fallidos'):
                db_usuario.intentos_fallidos = usuario.intentos_fallidos
            if hasattr(usuario, 'bloqueado_hasta'):
                db_usuario.bloqueado_hasta = usuario.bloqueado_hasta
            if hasattr(usuario, 'ultimo_intento_fallido'):
                db_usuario.ultimo_intento_fallido = usuario.ultimo_intento_fallido
            
            self.session.flush()
            return self._to_entity(db_usuario)
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Error al actualizar el usuario: {e}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error inesperado al actualizar usuario: {e}")

    def delete(self, usuario_id: int) -> bool:
        """
        Elimina un usuario de la base de datos.
        
        Args:
            usuario_id: ID del usuario a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no se encontró el usuario
            
        Raises:
            Exception: Si ocurre un error durante la eliminación
        """
        if not usuario_id:
            return False
            
        try:
            db_usuario = self.session.get(UsuarioModel, usuario_id)
            if not db_usuario:
                return False
                
            self.session.delete(db_usuario)
            self.session.flush()
            return True
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Error al eliminar el usuario: {e}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error inesperado al eliminar usuario: {e}")
        """Elimina un usuario por su ID."""
        db_usuario = self.session.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()

    def get_usuarios_by_corredor(self, corredor_numero: int, skip: int = 0, limit: int = 100) -> List[UsuarioEntity]:
        """
        Obtiene los usuarios asociados a un corredor específico.
        
        Args:
            corredor_numero: Número de corredor para filtrar
            skip: Número de registros a omitir (para paginación)
            limit: Número máximo de registros a devolver
            
        Returns:
            List[UsuarioEntity]: Lista de entidades de usuario asociadas al corredor
            
        Raises:
            Exception: Si ocurre un error durante la consulta
        """
        try:
            db_usuarios = (
                self._get_base_query()
                .filter(UsuarioModel.corredor_numero == corredor_numero)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [self._to_entity(u) for u in db_usuarios if u is not None]
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener usuarios del corredor {corredor_numero}: {e}")

    def get_hashed_password(self, usuario_id: int) -> Optional[str]:
        """
        Obtiene la contraseña hasheada de un usuario.
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Optional[str]: Contraseña hasheada o None si el usuario no existe
        """
        try:
            db_usuario = self.session.get(UsuarioModel, usuario_id)
            return db_usuario.hashed_password if db_usuario else None
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener la contraseña del usuario: {e}")

    def registrar_intento_fallido(self, usuario_id: int) -> Optional[UsuarioEntity]:
        """
        Registra un intento fallido de inicio de sesión para un usuario.
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Optional[UsuarioEntity]: Entidad de usuario actualizada o None si no se encontró el usuario
        """
        try:
            db_usuario = self.session.get(UsuarioModel, usuario_id)
            if not db_usuario:
                return None
                
            # Inicializar contador si es necesario
            if db_usuario.intentos_fallidos is None:
                db_usuario.intentos_fallidos = 0
                
            # Incrementar contador y actualizar último intento
            db_usuario.intentos_fallidos += 1
            db_usuario.ultimo_intento_fallido = self._get_utc_now()
            
            self.session.flush()
            return self._to_entity(db_usuario)
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Error al registrar intento fallido: {e}")

    def reiniciar_intentos_fallidos(self, usuario_id: int) -> Optional[UsuarioEntity]:
        """
        Reinicia el contador de intentos fallidos de un usuario.
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Optional[UsuarioEntity]: Entidad de usuario actualizada o None si no se encontró el usuario
        """
        try:
            db_usuario = self.session.get(UsuarioModel, usuario_id)
            if not db_usuario:
                return None
                
            db_usuario.intentos_fallidos = 0
            db_usuario.ultimo_intento_fallido = None
            db_usuario.fecha_modificacion = self._get_utc_now()
            
            self.session.flush()
            return self._to_entity(db_usuario)
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Error al reiniciar intentos fallidos: {e}")

    def bloquear_usuario(self, usuario_id: int, hasta: datetime) -> Optional[UsuarioEntity]:
        """
        Bloquea un usuario hasta la fecha especificada.
        
        Args:
            usuario_id: ID del usuario a bloquear
            hasta: Fecha hasta la cual se bloqueará el usuario
            
        Returns:
            Optional[UsuarioEntity]: Entidad de usuario actualizada o None si no se encontró el usuario
        """
        try:
            db_usuario = self.session.get(UsuarioModel, usuario_id)
            if not db_usuario:
                return None
                
            db_usuario.bloqueado_hasta = hasta
            db_usuario.fecha_modificacion = self._get_utc_now()
            
            self.session.flush()
            return self._to_entity(db_usuario)
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Error al bloquear usuario: {e}")

    def desbloquear_usuario(self, usuario_id: int) -> Optional[UsuarioEntity]:
        """
        Desbloquea un usuario.
        
        Args:
            usuario_id: ID del usuario a desbloquear
            
        Returns:
            Optional[UsuarioEntity]: Entidad de usuario actualizada o None si no se encontró el usuario
        """
        try:
            db_usuario = self.session.get(UsuarioModel, usuario_id)
            if not db_usuario:
                return None
                
            db_usuario.bloqueado_hasta = None
            db_usuario.intentos_fallidos = 0  # También reiniciamos los intentos fallidos
            db_usuario.fecha_modificacion = self._get_utc_now()
            
            self.session.flush()
            return self._to_entity(db_usuario)
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Error al desbloquear usuario: {e}")

    def update_password(self, usuario_id: int, hashed_password: str) -> Optional[UsuarioEntity]:
        """
        Actualiza la contraseña hasheada de un usuario.
        
        Args:
            usuario_id: ID del usuario
            hashed_password: Nueva contraseña hasheada
            
        Returns:
            Optional[UsuarioEntity]: Entidad de usuario actualizada o None si no se encontró el usuario
        """
        try:
            db_usuario = self.session.get(UsuarioModel, usuario_id)
            if not db_usuario:
                return None
                
            db_usuario.hashed_password = hashed_password
            db_usuario.fecha_modificacion = self._get_utc_now()
            
            # Si el usuario estaba bloqueado por intentos fallidos, lo desbloqueamos
            if db_usuario.intentos_fallidos and db_usuario.intentos_fallidos > 0:
                db_usuario.intentos_fallidos = 0
                db_usuario.bloqueado_hasta = None
            
            self.session.flush()
            return self._to_entity(db_usuario)
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Error al actualizar la contraseña: {e}")
