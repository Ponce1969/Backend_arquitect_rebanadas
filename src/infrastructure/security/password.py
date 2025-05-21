from passlib.context import CryptContext
from argon2 import PasswordHasher
import warnings

# Mantenemos el contexto bcrypt por compatibilidad con hashes existentes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Argon2PasswordHelper:
    """Implementación de hashing y verificación de contraseñas usando Argon2."""
    
    def __init__(self):
        self.ph = PasswordHasher()
    
    def hash_password(self, password: str) -> str:
        """Hashea una contraseña usando Argon2."""
        return self.ph.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica si una contraseña plana coincide con un hash Argon2."""
        try:
            # Argon2 espera primero el hash y luego la contraseña (parámetros correctos)
            return self.ph.verify(hashed_password, plain_password)
        except Exception:
            return False


class PasswordHelper:
    """Utilidad para hashing y verificación de contraseñas.
    
    Esta clase actua como fachada que utiliza Argon2 para nuevos hashes,
    pero mantiene compatibilidad con hashes bcrypt existentes.
    """
    
    # Singleton de Argon2PasswordHelper para reutilización
    _argon2_helper = Argon2PasswordHelper()

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashea una contraseña usando Argon2."""
        # Usamos el helper de Argon2 para todos los nuevos hashes
        return PasswordHelper._argon2_helper.hash_password(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica si una contraseña plana coincide con un hash.
        
        Compatible con hashes de Argon2 y bcrypt.
        """
        # Detectamos si es un hash de Argon2 (comienza con $argon2)
        if hashed_password.startswith('$argon2'):
            return PasswordHelper._argon2_helper.verify_password(plain_password, hashed_password)
        # Fallback a bcrypt para compatibilidad con hashes existentes
        else:
            warnings.warn(
                "Usando bcrypt para verificar contraseña. Considere actualizar a Argon2 en el próximo inicio de sesión.",
                DeprecationWarning, stacklevel=2
            )
            return pwd_context.verify(plain_password, hashed_password)
