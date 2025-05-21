#!/usr/bin/env python3
"""
Script para verificar la configuración del sistema y dependencias.

Este script verifica que todas las dependencias necesarias estén instaladas
correctamente y que la configuración del sistema sea la adecuada.
"""
import sys
import json
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Tuple

# Versiones mínimas requeridas
MIN_PYTHON = (3, 10)
MIN_POETRY = "1.3.0"
MIN_DOCKER = "20.10.0"
MIN_DOCKER_COMPOSE = "1.29.0"

# Configuración de rutas
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
REQUIREMENTS_TXT = PROJECT_ROOT / "requirements.txt"
PYPROJECT_TOML = PROJECT_ROOT / "pyproject.toml"

# Añadir el directorio raíz al path para importaciones absolutas
sys.path.append(str(PROJECT_ROOT))

class Colors:
    """Códigos de colores ANSI para la salida en consola."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str) -> None:
    """Imprime un encabezado con formato."""
    print(f"\n{Colors.HEADER}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * 80}{Colors.ENDC}\n")

def print_success(text: str) -> None:
    """Imprime un mensaje de éxito."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_warning(text: str) -> None:
    """Imprime una advertencia."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text: str) -> None:
    """Imprime un mensaje de error."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def check_python_version() -> Tuple[bool, str]:
    """Verifica la versión de Python."""
    current_version = sys.version_info
    version_str = f"{current_version.major}.{current_version.minor}.{current_version.micro}"
    
    if current_version >= MIN_PYTHON:
        return True, "Python {} (>= {})".format(version_str, '.'.join(map(str, MIN_PYTHON)))
    else:
        return False, "Python {} (se requiere >= {})".format(version_str, '.'.join(map(str, MIN_PYTHON)))

def run_command(cmd: List[str]) -> Tuple[bool, str]:
    """Ejecuta un comando y devuelve el resultado."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        return False, str(e.stderr if hasattr(e, 'stderr') else str(e))

def check_poetry() -> Tuple[bool, str]:
    """Verifica si Poetry está instalado y su versión."""
    success, output = run_command(["poetry", "--version"])
    if not success:
        return False, "Poetry no está instalado"
    
    # Extraer la versión de la salida
    version = output.split()[-1]
    if version >= MIN_POETRY:
        return True, f"Poetry {version} (>= {MIN_POETRY})"
    else:
        return False, f"Poetry {version} (se requiere >= {MIN_POETRY})"

def check_docker() -> Tuple[bool, str]:
    """Verifica si Docker está instalado y su versión."""
    success, output = run_command(["docker", "--version"])
    if not success:
        return False, "Docker no está instalado"
    
    # Extraer la versión de la salida
    version = output.split()[2].rstrip(',')
    if version >= MIN_DOCKER:
        return True, f"Docker {version} (>= {MIN_DOCKER})"
    else:
        return False, f"Docker {version} (se requiere >= {MIN_DOCKER})"

def check_docker_compose() -> Tuple[bool, str]:
    """Verifica si Docker Compose está instalado y su versión."""
    success, output = run_command(["docker-compose", "--version"])
    if not success:
        return False, "Docker Compose no está instalado"
    
    # Extraer la versión de la salida
    version = output.split()[2].rstrip(',')
    if version >= MIN_DOCKER_COMPOSE:
        return True, f"Docker Compose {version} (>= {MIN_DOCKER_COMPOSE})"
    else:
        return False, f"Docker Compose {version} (se requiere >= {MIN_DOCKER_COMPOSE})"

def check_requirements() -> Dict[str, Tuple[bool, str]]:
    """Verifica si los requisitos están instalados."""
    # Lista de paquetes requeridos con sus descripciones
    required_packages = {
        "sqlalchemy": "SQLAlchemy (ORM para base de datos)",
        "psycopg2-binary": "psycopg2 (Adaptador PostgreSQL para Python)",
        "pydantic": "Pydantic (Validación de datos)",
        "fastapi": "FastAPI (Framework web)",
        "uvicorn": "Uvicorn (Servidor ASGI)",
        "python-jose": "python-jose (JWT)",
        "passlib": "Passlib (Hashing de contraseñas)",
        "python-multipart": "python-multipart (Parseo de formularios)",
        "python-dotenv": "python-dotenv (Variables de entorno)",
        "alembic": "Alembic (Migraciones de base de datos)",
        "pytest": "pytest (Pruebas unitarias)",
        "httpx": "HTTPX (Cliente HTTP)",
        "email-validator": "email-validator (Validación de correos)",
    }
    
    # Ejecutar pip list para obtener los paquetes instalados
    success, output = run_command([sys.executable, "-m", "pip", "list", "--format=json"])
    
    if not success:
        return {"error": (False, "No se pudo obtener la lista de paquetes instalados")}
    
    # Procesar la salida de pip
    installed_packages = {}
    try:
        # Intentar con el formato JSON primero
        packages = json.loads(output)
        installed_packages = {pkg["name"].lower(): pkg["version"] for pkg in packages}
    except json.JSONDecodeError:
        # Fallback a formato legado
        for line in output.split('\n'):
            if not line.strip() or '---' in line:
                continue
                
            parts = line.split()
            if len(parts) >= 2:
                pkg_name = parts[0].lower()
                pkg_version = parts[1]
                installed_packages[pkg_name] = pkg_version
    
    # Verificar paquetes requeridos
    results: Dict[str, Tuple[bool, str]] = {}
    for pkg, desc in required_packages.items():
        if pkg in installed_packages:
            results[pkg] = (True, f"{desc}: {installed_packages[pkg]}")
        else:
            results[pkg] = (False, f"Falta instalar: {desc}")
    
    return results

def check_database_connection() -> Tuple[bool, str]:
    """Verifica la conexión a la base de datos."""
    try:
        import os
        from sqlalchemy import create_engine, text
        
        # Construir la URL de conexión desde las variables de entorno
        db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_SERVER')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "Conexión exitosa a la base de datos"
    except Exception as e:
        return False, f"Error de conexión a la base de datos: {str(e)}"

def check_environment_variables() -> Dict[str, Tuple[bool, str]]:
    """Verifica las variables de entorno requeridas."""
    required_vars = [
        ("POSTGRES_USER", "Usuario de PostgreSQL"),
        ("POSTGRES_PASSWORD", "Contraseña de PostgreSQL"),
        ("POSTGRES_DB", "Base de datos PostgreSQL"),
        ("POSTGRES_SERVER", "Servidor PostgreSQL"),
        ("POSTGRES_PORT", "Puerto PostgreSQL"),
        ("SECRET_KEY", "Clave secreta para JWT"),
        ("ACCESS_TOKEN_EXPIRE_MINUTES", "Tiempo de expiración de tokens")
    ]
    
    results: Dict[str, Tuple[bool, str]] = {}
    for var, description in required_vars:
        value = os.environ.get(var)
        if value:
            result = (True, f"{description}: {value[:10]}..." if len(str(value)) > 10 else f"{description}: {value}")
        else:
            result = (False, f"No definida: {description}")
        results[var] = result
        
    return results

def main():
    """Función principal."""
    print_header("VERIFICACIÓN DEL SISTEMA")
    
    # Verificar versión de Python
    print("\n1. Verificando versión de Python...")
    py_success, py_msg = check_python_version()
    if py_success:
        print_success(py_msg)
    else:
        print_error(py_msg)
    
    # Verificar Poetry
    print("\n2. Verificando Poetry...")
    poetry_success, poetry_msg = check_poetry()
    if poetry_success:
        print_success(poetry_msg)
    else:
        print_warning(poetry_msg)
    
    # Verificar Docker
    print("\n3. Verificando Docker...")
    docker_success, docker_msg = check_docker()
    if docker_success:
        print_success(docker_msg)
    else:
        print_warning(docker_msg)
    
    # Verificar Docker Compose
    print("\n4. Verificando Docker Compose...")
    compose_success, compose_msg = check_docker_compose()
    if compose_success:
        print_success(compose_msg)
    else:
        print_warning(compose_msg)
    
    # Verificar dependencias
    print("\n5. Verificando dependencias...")
    deps = check_requirements()
    
    if deps.get('error'):
        print_error(f"Error al verificar dependencias: {deps['error']}")
    else:
        for dep, (installed, info) in deps.items():
            if installed:
                print_success(f"✓ {info}")
            else:
                print_error(f"✗ {info}")
    
    # Verificar variables de entorno
    print("\n6. Verificando variables de entorno...")
    env_vars = check_environment_variables()
    for var, (is_set, msg) in env_vars.items():
        if is_set:
            print_success(msg)
        else:
            print_warning(msg)
    
    # Verificar conexión a la base de datos
    print("\n7. Verificando conexión a la base de datos...")
    db_success, db_msg = check_database_connection()
    if db_success:
        print_success(db_msg)
    else:
        print_error(db_msg)
    
    # Resumen
    print_header("RESUMEN")
    
    # Verificar si hay errores críticos
    critical_errors = [
        ("Python", py_success),
        ("Base de datos", db_success),
    ]
    
    has_critical_errors = any(not success for _, success in critical_errors)
    
    for component, success in critical_errors:
        status = "OK" if success else "ERROR"
        print(f"{component}: {status}")
    
    if has_critical_errors:
        print("\n[ERROR] Hay problemas críticos que deben resolverse antes de continuar.")
        sys.exit(1)
    else:
        print("\n[ÉXITO] La verificación del sistema se completó sin errores críticos.")
        print("        El sistema debería estar listo para funcionar correctamente.")

if __name__ == "__main__":
    main()
