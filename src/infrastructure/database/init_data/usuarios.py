from sqlalchemy.orm import Session

from src.features.usuarios.domain.types import Role
from src.features.usuarios.domain.entities import Usuario
from src.features.usuarios.infrastructure.models import Usuario as UsuarioModel
from src.infrastructure.security.password import PasswordHelper


def init_usuarios(db: Session) -> None:
    """Inicializa usuarios por defecto si no existen."""
    # Verificar si ya existen usuarios en la base de datos
    existing_users = db.query(UsuarioModel).count()
    if existing_users > 0:
        print(f"Ya existen {existing_users} usuarios en la base de datos. Omitiendo inicialización.")
        return

    # Crear el usuario administrador
    password_helper = PasswordHelper()
    hashed_password = password_helper.hash_password("Gallinal2218**")

    # Crear directamente el modelo SQLAlchemy
    db_admin = UsuarioModel(
        nombre="Rodrigo",
        apellido="Ponce",
        email="rpd.ramas@gmail.com",
        username="rponce",
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=True,
        role="admin",
        corredor_numero=None,
        comision_porcentaje=10.0,
        telefono=""
    )
    
    # Guardar en la base de datos
    db.add(db_admin)
    db.commit()
    print("Usuario administrador creado con éxito.")
