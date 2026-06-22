from fastapi import FastAPI
from app.config import settings

#Inicialización de FastAPI con metadatos del proyecto
app = FastAPI(
    title="File Forge API",
    description="Microservicio para la gestión y carga de archivos en el pipeline de datos",
    version="0.1.0",
)

#Endpoint de prueba
@app.get("/status", tags=["Salud"])
def status_check():
    """
    Endpoint simple para verificar que la api esta viva 
    y expone el entorno configurado
    """

    return {
        "status": "healthy",
        "environment": settings.app_env,
        "bucket_target": settings.aws_s3_bucket
    }

