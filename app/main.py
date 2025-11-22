from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import medicines, uber
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI(
    title="DIGEMID Medicine Search API",
    description="""
    API para buscar medicamentos en el Observatorio de Productos Farmacéuticos de DIGEMID.

    Esta API permite realizar búsquedas automatizadas de medicamentos, obteniendo información sobre:
    - Precios unitarios
    - Farmacias y boticas donde están disponibles
    - Laboratorios fabricantes
    - Fechas de actualización de precios

    ## Características
    - Búsqueda por nombre de medicamento
    - Filtrado por ubicación (departamento, provincia, distrito)
    - Resultados limitados y paginados
    - Web scraping automatizado con Selenium

    ## Tecnologías
    - FastAPI
    - Selenium WebDriver
    - Pydantic
    """,
    version="1.0.0",
    contact={
        "name": "Backend RIMAC",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(medicines.router)
app.include_router(uber.router)


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz de la API

    Returns:
        Información básica de la API
    """
    return {
        "message": "DIGEMID Medicine Search API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/medicines/health"
    }


@app.get("/health", tags=["Health"])
async def health():
    """
    Health check general de la aplicación

    Returns:
        Estado de la aplicación
    """
    return {
        "status": "healthy",
        "application": "DIGEMID Medicine Search API"
    }


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True
    )
