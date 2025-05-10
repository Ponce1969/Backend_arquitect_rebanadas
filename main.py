import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from infrastructure.database import Base, engine

# Importar routers
from features.aseguradoras.infrastructure.api.v1.aseguradoras_router import router as aseguradoras_router
from features.clientes.infrastructure.api.v1.clientes_router import router as clientes_router
from features.usuarios.infrastructure.api.v1.usuarios_router import router as usuarios_router

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


@app.get("/")
async def root():
    return {"message": f"Bienvenido a {settings.PROJECT_NAME}"}


# Para ejecutar la aplicaciu00f3n directamente con Python
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
