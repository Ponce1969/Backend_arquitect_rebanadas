# API REST Seguros

## Descripción

API REST para la gestión de seguros desarrollada con FastAPI, SQLAlchemy y PostgreSQL, siguiendo los principios de Clean Architecture y Vertical Slicing.

## Seguridad

### Bloqueo de Cuentas

El sistema implementa un mecanismo de bloqueo de cuentas para prevenir ataques de fuerza bruta:

- Después de 5 intentos fallidos de inicio de sesión, la cuenta se bloquea temporalmente.
- El tiempo de bloqueo predeterminado es de 30 minutos.
- Los intentos fallidos se reinician después de 1 hora de inactividad.
- Los administradores pueden desbloquear manualmente las cuentas bloqueadas.

### Contraseñas Seguras

Las contraseñas deben cumplir con los siguientes requisitos:

- Mínimo 8 caracteres
- Al menos una letra mayúscula
- Al menos una letra minúscula
- Al menos un número
- Al menos un carácter especial

## Arquitectura

El proyecto sigue una arquitectura limpia (Clean Architecture) combinada con vertical slicing (rebanado vertical). La estructura se organiza por características o dominios del negocio (features), donde cada slice contiene:

### Migración a Rebanadas Verticales

Actualmente el proyecto está en proceso de migración desde una arquitectura monolítica tradicional hacia una arquitectura de rebanadas verticales. Durante esta transición, se mantienen algunos archivos de compatibilidad que serán eliminados en futuras versiones.

Para más detalles sobre el proceso de migración y cómo actualizar tu código, consulta la [Guía de Migración](docs/migracion_arquitectura.md).

1. **Dominio (Domain)**: Entidades puras de negocio sin dependencias externas
2. **Aplicación (Application)**: Casos de uso e interfaces de repositorio
3. **Infraestructura (Infrastructure)**: Implementaciones concretas (modelos SQLAlchemy, repositorios, routers)

Las dependencias fluyen de afuera hacia adentro, nunca al revés. La inyección de dependencias se utiliza para conectar las capas sin violar este principio.

## Características Implementadas

- Gestión de monedas (CRUD completo)
- Gestión de tipos de documento (CRUD completo)
- Gestión de usuarios y autenticación
  - Autenticación JWT
  - Bloqueo de cuentas después de múltiples intentos fallidos
  - Reinicio de contraseña
- Gestión de corredores y clientes
- Validación robusta con Pydantic v2

## Scripts de Utilidad

El proyecto incluye varios scripts de utilidad organizados en el directorio `scripts/`:

### Seguridad (`scripts/security/`)
- `generate_security_report.py`: Genera informes de seguridad sobre intentos de inicio de sesión
- `monitor_logins.py`: Monitorea en tiempo real los intentos de inicio de sesión
- `test_audit_system.py`: Pruebas para el sistema de auditoría

### Utilidades (`scripts/utils/`)
- `check_system.py`: Verifica la configuración del sistema y dependencias
- `update_env.py`: Herramienta para actualizar variables de entorno

### Migraciones (`scripts/migrations/`)
- `account_lockout_migration.py`: Migración para el sistema de bloqueo de cuentas
- `setup_audit_tables.py`: Configura las tablas de auditoría

### Ejecución de scripts

Para ejecutar cualquiera de estos scripts, asegúrate de estar en el directorio raíz del proyecto y activa el entorno virtual de Poetry:

```bash
# Navegar al directorio del proyecto
cd /ruta/a/tu/proyecto

# Activar el entorno virtual de Poetry
poetry shell

# Ejecutar un script (ejemplo con check_system.py)
python -m scripts.utils.check_system
```

## Requisitos

- Python 3.10 o superior
- PostgreSQL
- Docker y Docker Compose (opcional, para desarrollo)

## Instalación y Configuración

### Clonar el repositorio

```bash
git clone https://github.com/Ponce1969/Backend_arquitect_rebanadas.git
cd Backend_arquitect_rebanadas
```

### Configuración del entorno

1. Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
# PostgreSQL
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seguros_db

# Seguridad
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_MINUTES=30
RESET_ATTEMPTS_AFTER_MINUTES=60

# FastAPI
API_PREFIX=/api/v1
PROJECT_NAME=API Seguros
BACKEND_CORS_ORIGINS=["http://localhost", "http://localhost:4200", "http://localhost:3000"]

# Seguridad
SECRET_KEY=tu_clave_secreta_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Usando Poetry (recomendado)

```bash
# Instalar Poetry si no lo tienes
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependencias
poetry install

# Activar entorno virtual
poetry shell
```

### Usando pip y venv

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate
# O en Windows
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Usando Docker

```bash
# Construir y levantar los contenedores
docker-compose up -d --build
```

## Ejecución

### Desarrollo local

```bash
# Ejecutar servidor de desarrollo
uvicorn main:app --reload
```

### Con Docker

```bash
# Si ya tienes los contenedores levantados, la API estará disponible en http://localhost:8000
```

## Documentación de la API

Una vez que el servidor esté en ejecución, puedes acceder a la documentación interactiva de la API en:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Pruebas

```bash
# Ejecutar pruebas
pytest

# Con cobertura
pytest --cov=src
```

## Herramientas de desarrollo

- **Ruff**: Linter para Python
- **Mypy**: Verificación estática de tipos
- **Pytest**: Framework de pruebas

## Contribución

1. Hacer fork del repositorio
2. Crear una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Hacer commit de tus cambios (`git commit -m 'feat: Add some amazing feature'`)
4. Hacer push a la rama (`git push origin feature/amazing-feature`)
5. Abrir un Pull Request

## Licencia

Distribuido bajo la licencia MIT. Ver `LICENSE` para más información.

