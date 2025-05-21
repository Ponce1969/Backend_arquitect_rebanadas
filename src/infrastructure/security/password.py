from passlib.context import CryptContext
from argon2 import PasswordHasher

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


class Argon2PasswordHelper:
    def __init__(self):
        self.ph = PasswordHasher()
    
    def hash_password(self, password: str) -> str:
        return self.ph.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            # Argon2 expects the hash first, then the password
            return self.ph.verify(hashed_password, plain_password)
        except Exception:
            return False
