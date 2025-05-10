import os
import sys
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Agregar el directorio src al path de Python
sys.path.append(os.path.abspath('src'))

from src.config.settings import settings
from src.infrastructure.database import Base, engine, get_db

# Importar routers
from src.features.aseguradoras.infrastructure.api.v1.aseguradoras_router import router as aseguradoras_router
from src.features.clientes.infrastructure.api.v1.clientes_router import router as clientes_router
from src.features.usuarios.infrastructure.api.v1.usuarios_router import router as usuarios_router

# Importar inicializadores de datos
from src.features.tipos_documento.infrastructure.init_data import init_tipos_documento
from src.features.corredores.infrastructure.init_data import init_corredores

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicaciu00f3n FastAPI
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
app.include_router(usuarios_router, prefix=settings.API_V1_STR)

# Evento de inicio para inicializar datos
@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    try:
        # Inicializar tipos de documento
        init_tipos_documento(db)
        # Inicializar corredores
        init_corredores(db)
    except Exception as e:
        print(f"Error al inicializar datos: {e}")
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": f"Bienvenido a {settings.PROJECT_NAME}"}


# Para ejecutar la aplicaciu00f3n directamente con Python
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
