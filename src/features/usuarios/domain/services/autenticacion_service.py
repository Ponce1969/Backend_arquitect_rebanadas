"""
Servicio de dominio para manejar la autenticación y bloqueo de cuentas.

Este servicio encapsula la lógica de negocio relacionada con la autenticación de usuarios,
validación de contraseñas y manejo de bloqueos de cuentas por intentos fallidos.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from argon2 import PasswordHasher

from src.features.usuarios.domain.entities import Usuario as UsuarioEntity
from src.features.usuarios.application.interfaces.repositories import AbstractUsuarioRepository
from src.infrastructure.security.password import PasswordHelper

# Configuración de bloqueo de cuentas
MAX_INTENTOS_FALLIDOS = 5
TIEMPO_BLOQUEO_MINUTOS = 30

ph = PasswordHasher()

class AutenticacionService:
    """
    Servicio de autenticación que maneja la lógica de negocio relacionada con:
    - Verificación de credenciales
    - Generación y verificación de hashes de contraseñas
    - Manejo de bloqueos de cuentas por intentos fallidos
    """

    def __init__(self, usuario_repository: AbstractUsuarioRepository):
        """
        Inicializa el servicio de autenticación con un repositorio de usuarios.
        
        Args:
            usuario_repository: Repositorio para acceder a los datos de usuarios
        """
        self.usuario_repository = usuario_repository

    def verificar_contrasena(
        self, contrasena_plana: str, hashed_password: str
    ) -> bool:
        """
        Verifica si una contraseña en texto plano coincide con su hash.
        
        Args:
            contrasena_plana: Contraseña en texto plano
            hashed_password: Hash de la contraseña almacenada
            
        Returns:
            bool: True si la contraseña es válida, False en caso contrario
        """
        try:
            # Argon2 espera primero el hash y luego la contraseña
            return ph.verify(hashed_password, contrasena_plana)
        except Exception as e:
            print(f"Error al verificar contraseña: {str(e)}")
            return False

    def obtener_hash_contrasena(self, contrasena: str) -> str:
        """
        Genera el hash de una contraseña.
        
        Args:
            contrasena: Contraseña en texto plano
            
        Returns:
            str: Hash de la contraseña
            
        Raises:
            ValueError: Si la contraseña está vacía
        """
        if not contrasena:
            raise ValueError("La contraseña no puede estar vacía")
            
        try:
            return ph.hash(contrasena)
        except Exception as e:
            print(f"Error al generar hash: {str(e)}")
            raise ValueError("Error al procesar la contraseña")

    def verificar_bloqueo_cuenta(self, usuario: UsuarioEntity) -> Tuple[bool, Optional[str]]:
        """
        Verifica si la cuenta de un usuario está bloqueada.
        
        Args:
            usuario: Entidad de usuario a verificar
            
        Returns:
            Tuple[bool, Optional[str]]: 
                - bool: True si la cuenta está bloqueada, False en caso contrario
                - str: Mensaje de error si la cuenta está bloqueada, None en caso contrario
        """
        if not usuario:
            return False, None
            
        ahora = datetime.now(timezone.utc)
        
        # Si la cuenta está bloqueada temporalmente
        if usuario.bloqueado_hasta and usuario.bloqueado_hasta > ahora:
            tiempo_restante = (usuario.bloqueado_hasta - ahora).seconds // 60
            return True, f"Cuenta bloqueada. Intente nuevamente en {tiempo_restante} minutos."
        
        # Si el tiempo de bloqueo ha expirado, reiniciamos el contador
        if usuario.bloqueado_hasta and usuario.bloqueado_hasta <= ahora:
            self._reiniciar_intentos_fallidos(usuario)
            
        return False, None

    def registrar_intento_fallido(self, usuario: UsuarioEntity) -> None:
        """
        Registra un intento fallido de inicio de sesión.
        
        Args:
            usuario: Entidad de usuario que intentó autenticarse
            
        Raises:
            ValueError: Si el usuario no es válido
        """
        if not usuario:
            raise ValueError("El usuario no puede ser None")
            
        ahora = datetime.now(timezone.utc)
        
        # Si ha pasado más de 1 hora desde el último intento, reiniciamos el contador
        if usuario.ultimo_intento_fallido and (ahora - usuario.ultimo_intento_fallido).seconds > 3600:
            usuario.intentos_fallidos = 0
        
        # Incrementamos el contador de intentos fallidos
        usuario.intentos_fallidos += 1
        usuario.ultimo_intento_fallido = ahora
        
        # Si se supera el límite de intentos, bloqueamos la cuenta
        if usuario.intentos_fallidos >= MAX_INTENTOS_FALLIDOS:
            usuario.bloqueado_hasta = ahora + timedelta(minutes=TIEMPO_BLOQUEO_MINUTOS)
        
        # Actualizamos el usuario en la base de datos
        self.usuario_repository.update(usuario)
    
    def _reiniciar_intentos_fallidos(self, usuario: UsuarioEntity) -> None:
        """
        Reinicia el contador de intentos fallidos de un usuario.
        
        Args:
            usuario: Entidad de usuario a actualizar
            
        Raises:
            ValueError: Si el usuario no es válido
        """
        if not usuario:
            raise ValueError("El usuario no puede ser None")
            
        usuario.intentos_fallidos = 0
        usuario.ultimo_intento_fallido = None
        usuario.bloqueado_hasta = None
        self.usuario_repository.update(usuario)
    
    def _actualizar_hash_si_es_necesario(self, usuario: UsuarioEntity, contrasena: str) -> None:
        """
        Actualiza el hash de la contraseña de un usuario si es necesario.
        
        Args:
            usuario: Entidad de usuario a actualizar
            contrasena: Contraseña en texto plano
            
        Raises:
            ValueError: Si el usuario no es válido
        """
        if not usuario:
            raise ValueError("El usuario no puede ser None")
            
        # Verificar si el hash es bcrypt
        if usuario.hashed_password.startswith("$2b$"):
            # Actualizar el hash a Argon2
            usuario.hashed_password = self.obtener_hash_contrasena(contrasena)
            self.usuario_repository.update(usuario)

    def autenticar_usuario(
        self, username: str, contrasena: str
    ) -> Tuple[Optional[UsuarioEntity], Optional[str]]:
        """
        Autentica a un usuario con su nombre de usuario y contraseña.
        
        Este método maneja toda la lógica de autenticación, incluyendo:
        - Búsqueda del usuario
        - Verificación de bloqueo de cuenta
        - Validación de credenciales
        - Manejo de intentos fallidos
        
        Args:
            username: Nombre de usuario
            contrasena: Contraseña en texto plano
            
        Returns:
            Tuple[Optional[UsuarioEntity], Optional[str]]: 
                - Usuario autenticado si las credenciales son válidas, None en caso contrario
                - Mensaje de error si la autenticación falla, None si es exitosa
                
        Example:
            >>> usuario, error = servicio.autenticar_usuario("usuario", "contraseña")
            >>> if usuario:
            ...     print(f"Bienvenido {usuario.nombre}")
            ... else:
            ...     print(f"Error: {error}")
        """
        if not username or not contrasena:
            return None, "Se requieren nombre de usuario y contraseña"
        
        # Buscar al usuario por nombre de usuario
        usuario = self.usuario_repository.get_by_username(username)
        if not usuario:
            # No revelamos que el usuario no existe por seguridad
            return None, "Credenciales inválidas"
        
        # Verificar si la cuenta está bloqueada
        bloqueado, mensaje_bloqueo = self.verificar_bloqueo_cuenta(usuario)
        if bloqueado:
            return None, mensaje_bloqueo
        
        # Verificar la contraseña
        contrasena_valida = self.verificar_contrasena(contrasena, usuario.hashed_password)
        
        if not contrasena_valida:
            # Registrar el intento fallido
            self.registrar_intento_fallido(usuario)
            return None, "Credenciales inválidas"
        
        # Autenticación exitosa, reiniciar intentos fallidos
        self._reiniciar_intentos_fallidos(usuario)
        
        # Si el hash es bcrypt, actualizarlo a Argon2
        self._actualizar_hash_si_es_necesario(usuario, contrasena)
        
        # Si la cuenta está inactiva
        if not usuario.is_active:
            return None, "La cuenta está deshabilitada"
        
        return usuario, None
