from sqlalchemy.orm import Session

from src.features.usuarios.infrastructure.models import Usuario as UsuarioModel
from src.infrastructure.security.password import Argon2PasswordHelper


def init_usuarios(db: Session) -> None:
    """Inicializa usuarios por defecto si no existen."""
    try:
        # Verificar si el usuario administrador ya existe
        admin = db.query(UsuarioModel).filter(UsuarioModel.username == "rponce").first()
        if admin:
            print("El usuario administrador ya existe en la base de datos.")
            return

        print("Creando usuario administrador...")
        # Crear el usuario administrador
        password_helper = Argon2PasswordHelper()
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
        
    except Exception as e:
        db.rollback()
        print(f"Error al crear usuario administrador: {str(e)}")
        raise
