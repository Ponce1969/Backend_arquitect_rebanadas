from passlib.context import CryptContext

# Configura el contexto de hashing (bcrypt es común)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHelper:
    """Utilidad para hashing y verificación de contraseñas."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashea una contraseña."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica si una contraseña plana coincide con una hashed."""
        return pwd_context.verify(plain_password, hashed_password)
