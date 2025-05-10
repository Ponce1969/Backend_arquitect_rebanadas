
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from ..application.interfaces.repositories import AbstractUsuarioRepository
from ..domain.entities import Usuario as UsuarioEntity
from .models import Usuario as UsuarioModel


class SQLAlchemyUsuarioRepository(AbstractUsuarioRepository):
    """Implementación del Repositorio de Usuarios usando SQLAlchemy."""

    def __init__(self, session: Session):
        self.session = session

    # Helper para query base con eager loading del Corredor asociado
    def _get_base_query(self):
        return self.session.query(UsuarioModel).options(
            joinedload(UsuarioModel.corredor_rel)  # Eager load Corredor si está asociado
        )

    def add(self, usuario: UsuarioEntity, hashed_password: str) -> UsuarioEntity:
        """Añade un nuevo usuario a la DB."""
        # La contraseña ya viene hasheada desde el caso de uso

        try:
            # Verificamos si ya existe un usuario con el mismo username o email
            existing_username = self.get_by_username(usuario.username)
            if existing_username:
                raise ValueError(f"El nombre de usuario '{usuario.username}' ya está en uso.")

            existing_email = self.get_by_email(usuario.email)
            if existing_email:
                raise ValueError(f"El correo electrónico '{usuario.email}' ya está en uso.")

            # Creamos el modelo a partir de la entidad y asignamos la contraseña hasheada
            db_usuario = UsuarioModel.from_entity(usuario)
            db_usuario.hashed_password = hashed_password
            
            self.session.add(db_usuario)
            self.session.flush()  # Para obtener el ID generado
            
            # Actualizamos el ID en la entidad de dominio
            usuario.id = db_usuario.id
            
            return usuario
        except IntegrityError as e:
            self.session.rollback()
            # Manejar errores específicos (ej. username/email duplicado)
            raise ValueError(f"Error de integridad al crear usuario: {e}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error al crear usuario: {e}")

    def get_by_id(self, usuario_id: int) -> UsuarioEntity | None:
        """Obtiene un usuario de la DB por su ID, con relaciones cargadas."""
        db_usuario = self._get_base_query().filter(UsuarioModel.id == usuario_id).first()
        if db_usuario:
            return db_usuario.to_entity()  # Mapeo de Modelo a Entidad
        return None

    def get_by_username(self, username: str) -> UsuarioEntity | None:
        """Obtiene un usuario por su nombre de usuario, con relaciones cargadas."""
        db_usuario = self._get_base_query().filter(UsuarioModel.username == username).first()
        if db_usuario:
            return db_usuario.to_entity()
        return None

    def get_by_email(self, email: str) -> UsuarioEntity | None:
        """Obtiene un usuario por su correo electrónico, con relaciones cargadas."""
        db_usuario = self._get_base_query().filter(UsuarioModel.email == email).first()
        if db_usuario:
            return db_usuario.to_entity()
        return None

    def get_all(self) -> list[UsuarioEntity]:
        """Obtiene todos los usuarios, con relaciones cargadas."""
        db_usuarios = self._get_base_query().all()
        return [db_usuario.to_entity() for db_usuario in db_usuarios]

    def update(self, usuario: UsuarioEntity) -> UsuarioEntity:
        """Actualiza un usuario existente."""
        db_usuario = self.session.query(UsuarioModel).filter(UsuarioModel.id == usuario.id).first()
        if not db_usuario:
            raise ValueError(f"Usuario con ID {usuario.id} no encontrado.")

        # Verificar si el nuevo username ya está en uso por otro usuario
        if usuario.username != db_usuario.username:
            existing = self.session.query(UsuarioModel).filter(
                UsuarioModel.username == usuario.username,
                UsuarioModel.id != usuario.id
            ).first()
            if existing:
                raise ValueError(f"El nombre de usuario '{usuario.username}' ya está en uso.")

        # Verificar si el nuevo email ya está en uso por otro usuario
        if usuario.email != db_usuario.email:
            existing = self.session.query(UsuarioModel).filter(
                UsuarioModel.email == usuario.email,
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
        db_usuario.role = usuario.role.value
        db_usuario.corredor_numero = usuario.corredor_numero
        db_usuario.comision_porcentaje = usuario.comision_porcentaje
        db_usuario.telefono = usuario.telefono
        # No actualizamos fecha_creacion
        # fecha_modificacion se actualiza automáticamente por onupdate

        self.session.flush()
        return db_usuario.to_entity()

    def delete(self, usuario_id: int) -> bool:
        """Elimina un usuario por su ID."""
        db_usuario = self.session.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
        if db_usuario:
            self.session.delete(db_usuario)
            return True
        return False

    def get_usuarios_by_corredor(self, corredor_numero: int) -> list[UsuarioEntity]:
        """Obtiene usuarios asociados a un corredor específico, con relaciones cargadas."""
        db_usuarios = self._get_base_query().filter(UsuarioModel.corredor_numero == corredor_numero).all()
        return [db_usuario.to_entity() for db_usuario in db_usuarios]

    def get_hashed_password(self, usuario_id: int) -> str | None:
        """Obtiene la contraseña hasheada de un usuario por su ID."""
        db_usuario = self.session.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
        if db_usuario:
            return db_usuario.hashed_password
        return None
        
    def update_password(self, usuario_id: int, hashed_password: str) -> bool:
        """Actualiza la contraseña hasheada de un usuario."""
        db_usuario = self.session.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
        if not db_usuario:
            return False
            
        db_usuario.hashed_password = hashed_password
        self.session.flush()
        return True
