"""
Script para agregar columnas de bloqueo de cuenta a la tabla de usuarios.

Este script debe ejecutarse manualmente con permisos de superusuario en la base de datos.
"""

import os
import sys
from sqlalchemy import create_engine, text

def run_migration():
    """Ejecuta la migración para agregar columnas de bloqueo de cuenta."""
    try:
        import os
        from sqlalchemy import create_engine, text
        
        # Construir la URL de conexión desde las variables de entorno
        db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_SERVER')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        
        # Crear conexión a la base de datos
        engine = create_engine(db_url)
        
        # Ejecutar las migraciones
        with engine.connect() as conn:
            # Agregar columnas
            conn.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN IF NOT EXISTS intentos_fallidos INTEGER NOT NULL DEFAULT 0,
                ADD COLUMN IF NOT EXISTS bloqueado_hasta TIMESTAMP WITH TIME ZONE,
                ADD COLUMN IF NOT EXISTS ultimo_intento_fallido TIMESTAMP WITH TIME ZONE;
                """))
            
            # Agregar comentarios
            conn.execute(text("""
                COMMENT ON COLUMN usuarios.intentos_fallidos IS 'Número de intentos fallidos de inicio de sesión';
                COMMENT ON COLUMN usuarios.bloqueado_hasta IS 'Hasta cuándo está bloqueada la cuenta (None si no está bloqueada)';
                COMMENT ON COLUMN usuarios.ultimo_intento_fallido IS 'Cuándo fue el último intento fallido de inicio de sesión';
                """))
            
            # Crear índices
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_usuarios_bloqueado_hasta 
                ON usuarios(bloqueado_hasta);
                
                CREATE INDEX IF NOT EXISTS ix_usuarios_ultimo_intento_fallido 
                ON usuarios(ultimo_intento_fallido);
                """))
            
            conn.commit()
        
        print("Migración completada exitosamente.")
        return True
    except Exception as e:
        print(f"Error al ejecutar la migración: {e}")
        return False

if __name__ == "__main__":
    run_migration()
