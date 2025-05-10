FROM python:3.12-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN python -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==$POETRY_VERSION

# Agregar Poetry al PATH
ENV PATH="${POETRY_VENV}/bin:${PATH}"

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración de Poetry
COPY pyproject.toml poetry.lock* ./

# Configurar Poetry para no crear un entorno virtual
RUN poetry config virtualenvs.create false

# Instalar dependencias
RUN poetry install --no-interaction --no-ansi --no-root

# Copiar el código fuente
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
