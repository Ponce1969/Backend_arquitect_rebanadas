import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Agregar el directorio src al path de Python
sys.path.append(os.path.abspath('src'))

from src.config.settings import settings
from src.infrastructure.database import Base, engine, get_db

# Importar routers
from src.features.aseguradoras.infrastructure.api.v1.aseguradoras_router import router as aseguradoras_router
from src.features.clientes.infrastructure.api.v1.clientes_router import router as clientes_router
from src.features.corredores.infrastructure.api.v1.corredores_router import router as corredores_router
from src.features.sustituciones_corredores.infrastructure.api.v1.sustituciones_router import router as sustituciones_corredores_router
from src.features.usuarios.infrastructure.api.v1.usuarios_router import router as usuarios_router
from src.features.polizas.infrastructure.api.v1.polizas_router import router as polizas_router
from src.features.tipos_seguros.infrastructure.api.v1.tipos_seguro_router import router as tipos_seguro_router

# Importar inicializadores de datos
from src.infrastructure.database.init_data import init_tipos_documento, init_usuarios
from src.features.corredores.infrastructure.init_data import init_corredores

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configurar CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Incluir routers
app.include_router(aseguradoras_router, prefix=settings.API_V1_STR)
app.include_router(clientes_router, prefix=settings.API_V1_STR)
app.include_router(corredores_router, prefix=settings.API_V1_STR)
app.include_router(sustituciones_corredores_router, prefix=settings.API_V1_STR)
app.include_router(usuarios_router, prefix=settings.API_V1_STR)
app.include_router(polizas_router, prefix=settings.API_V1_STR)
app.include_router(tipos_seguro_router, prefix=settings.API_V1_STR)

# Evento de inicio para inicializar datos
@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    try:
        # Inicializar tipos de documento
        init_tipos_documento(db)
        # Inicializar corredores
        init_corredores(db)
        # Inicializar usuarios
        init_usuarios(db)
    except Exception as e:
        print(f"Error al inicializar datos: {e}")
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": f"Bienvenido a {settings.PROJECT_NAME}"}


# Para ejecutar la aplicación directamente con Python
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
