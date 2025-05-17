# API REST Seguros

## Descripción

API REST para la gestión de seguros desarrollada con FastAPI, SQLAlchemy y PostgreSQL, siguiendo los principios de Clean Architecture y Vertical Slicing.

## Arquitectura

El proyecto sigue una arquitectura limpia (Clean Architecture) combinada con vertical slicing (rebanado vertical). La estructura se organiza por características o dominios del negocio (features), donde cada slice contiene:

1. **Dominio (Domain)**: Entidades puras de negocio sin dependencias externas
2. **Aplicación (Application)**: Casos de uso e interfaces de repositorio
3. **Infraestructura (Infrastructure)**: Implementaciones concretas (modelos SQLAlchemy, repositorios, routers)

Las dependencias fluyen de afuera hacia adentro, nunca al revés. La inyección de dependencias se utiliza para conectar las capas sin violar este principio.

## Características Implementadas

- Gestión de monedas (CRUD completo)
- Gestión de tipos de documento (CRUD completo)
- Gestión de usuarios y autenticación
- Gestión de corredores y clientes
- Validación robusta con Pydantic v2

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

