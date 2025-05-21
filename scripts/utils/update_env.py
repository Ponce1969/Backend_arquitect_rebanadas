#!/usr/bin/env python3
"""
Script para actualizar automáticamente las variables de entorno relacionadas con el bloqueo de cuentas.

Este script busca el archivo .env en el directorio del proyecto y actualiza o agrega
las variables necesarias para el bloqueo de cuentas.

Uso:
    python update_env.py [--path RUTA_AL_PROYECTO]
"""
import re
import sys
from pathlib import Path

# Configuración por defecto
DEFAULT_ENV_VARS = {
    "# Configuración de bloqueo de cuentas": "",
    "MAX_LOGIN_ATTEMPTS": "5",
    "ACCOUNT_LOCKOUT_MINUTES": "30",
    "RESET_ATTEMPTS_AFTER_MINUTES": "60",
}

def find_env_file(project_path=None):
    """Busca el archivo .env en el directorio del proyecto."""
    if project_path:
        possible_paths = [Path(project_path).absolute()]
    else:
        # Buscar primero en el directorio raíz del proyecto (tres niveles arriba de este script)
        script_dir = Path(__file__).parent.absolute()
        project_root = script_dir.parent.parent.parent
        
        # Buscar en el directorio raíz del proyecto y en el directorio actual
        possible_paths = [
            project_root,
            Path.cwd(),
            current_dir.parent,
            current_dir.parent.parent,
        ]
    
    for path in possible_paths:
        env_path = path / ".env"
        if env_path.exists():
            return env_path
    
    return None

def update_env_file(env_path):
    """Actualiza el archivo .env con las variables necesarias."""
    # Leer el contenido actual del archivo
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] No se pudo leer el archivo {env_path}: {e}")
        return False
    
    # Actualizar o agregar cada variable
    updated = False
    
    for comment, value in DEFAULT_ENV_VARS.items():
        if comment.startswith('#'):
            # Es un comentario, verificar si ya existe
            if comment not in content:
                content += f"\n\n{comment}"
                updated = True
            continue
            
        # Es una variable de entorno
        pattern = re.compile(f'^{comment}=.*$', re.MULTILINE)
        
        if pattern.search(content):
            # La variable ya existe, actualizar su valor
            new_content = pattern.sub(f"{comment}={value}", content, count=1)
            if new_content != content:
                content = new_content
                updated = True
        else:
            # Agregar la nueva variable
            content += f"\n{comment}={value}"
            updated = True
    
    # Escribir el contenido actualizado
    if updated:
        try:
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[ÉXITO] Archivo {env_path} actualizado correctamente.")
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo escribir en el archivo {env_path}: {e}")
            return False
    else:
        print("[INFO] No se realizaron cambios en el archivo .env")
        return True

def main():
    """Función principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Actualiza las variables de entorno para el bloqueo de cuentas.')
    parser.add_argument('--path', help='Ruta al directorio del proyecto que contiene el archivo .env')
    args = parser.parse_args()
    
    # Buscar el archivo .env
    env_path = find_env_file(args.path)
    
    if not env_path:
        print("[ERROR] No se encontró el archivo .env en el directorio actual ni en los directorios superiores.")
        print("        Especifique la ruta al directorio del proyecto con --path")
        sys.exit(1)
    
    print(f"[INFO] Archivo .env encontrado en: {env_path}")
    
    # Actualizar el archivo .env
    success = update_env_file(env_path)
    
    if not success:
        print("\n[ERROR] No se pudo actualizar el archivo .env. Verifica los permisos e inténtalo de nuevo.")
        sys.exit(1)
    
    # Mostrar resumen de las variables
    print("\nVariables de entorno configuradas:")
    print("-" * 50)
    for var, value in DEFAULT_ENV_VARS.items():
        if var.startswith('#'):
            print(f"\n{var}")
        else:
            print(f"{var}={value}")
    
    print("\n[ÉXITO] Configuración completada. Reinicia el servidor para aplicar los cambios.")

if __name__ == "__main__":
    main()
