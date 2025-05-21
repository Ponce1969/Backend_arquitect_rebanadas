import os
import sys
import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agregar el directorio src al path de Python
sys.path.append(os.path.abspath('src'))

from src.config.settings import settings
from src.infrastructure.database import Base, engine, get_db
from src.domain.shared.exceptions import global_exception_handler, APIError

# Importar routers
from src.features.aseguradoras.infrastructure.api.v1.aseguradoras_router import router as aseguradoras_router
from src.features.clientes.infrastructure.api.v1.clientes_router import router as clientes_router
from src.features.corredores.infrastructure.api.v1.corredores_router import router as corredores_router
from src.features.sustituciones_corredores.infrastructure.api.v1.sustituciones_router import router as sustituciones_corredores_router
from src.features.usuarios.infrastructure.api.v1.usuarios_router import router as usuarios_router
from src.features.polizas.infrastructure.api.v1.polizas_router import router as polizas_router
from src.features.tipos_seguros.infrastructure.api.v1.tipos_seguro_router import router as tipos_seguro_router
from src.features.monedas.infrastructure.api.v1.monedas_router import router as monedas_router
from src.features.tipos_documento.infrastructure.api.v1.tipos_documento_router import router as tipos_documento_router
from src.features.corredores.infrastructure.api.v1.clientes_corredores_router import router as clientes_corredores_router

# Importar inicializadores de datos
from src.features.tipos_documento.infrastructure.init_data import init_tipos_documento
from src.features.monedas.infrastructure.init_data import init_monedas
from src.features.corredores.infrastructure.init_data import init_corredores
from src.infrastructure.database.init_data.usuarios import init_usuarios

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Middleware para manejar excepciones
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except APIError as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except RequestValidationError as e:
        return JSONResponse(status_code=422, content={"message": "Error de validación", "errors": e.errors()})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error interno del servidor"})

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
app.include_router(
    usuarios_router,
    prefix=settings.API_V1_STR
)
app.include_router(polizas_router, prefix=settings.API_V1_STR)
app.include_router(tipos_seguro_router, prefix=settings.API_V1_STR)
app.include_router(monedas_router, prefix=settings.API_V1_STR)
app.include_router(tipos_documento_router, prefix=settings.API_V1_STR)
app.include_router(clientes_corredores_router, prefix=settings.API_V1_STR)

# Configuración del ciclo de vida de la aplicación (eventos startup y shutdown)
@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando aplicación...")
    
    # Crear tablas en la base de datos si no existen
    try:
        logger.info("Creando tablas en la base de datos si no existen...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas correctamente")
    except Exception as e:
        logger.error(f"Error al crear tablas: {str(e)}")
        # No lanzamos la excepción para permitir que la aplicación inicie
    
    # Inicializar datos
    db = next(get_db())
    try:
        logger.info("Inicializando datos...")
        
        # Inicializar tipos de documento
        init_tipos_documento(db)
        logger.info("Tipos de documento inicializados correctamente")
        
        # Inicializar monedas
        init_monedas(db)
        logger.info("Monedas inicializadas correctamente")
        
        # Inicializar corredores
        init_corredores(db)
        logger.info("Corredores inicializados correctamente")
        
        # Inicializar usuarios
        init_usuarios(db)
        logger.info("Usuarios inicializados correctamente")
        
        logger.info("Todos los datos inicializados correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar datos: {str(e)}")
        # Capturamos la excepción para que la aplicación pueda iniciar aún con errores
    finally:
        db.close()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Cerrando la aplicación...")


@app.get("/")
async def root():
    return {"message": f"Bienvenido a {settings.PROJECT_NAME}"}


# Para ejecutar la aplicación directamente con Python
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
