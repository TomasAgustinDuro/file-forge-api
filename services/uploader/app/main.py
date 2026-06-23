from fastapi import FastAPI, UploadFile, File, HTTPException
from app.config import settings
from app.services.s3_storage import S3StorageService

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


@app.post("/files/upload", tags=["Carga"])
async def upload_file(file: UploadFile = File( ... )):
    """
    Endpoint de carga de archivo
    """

    storage_service = S3StorageService()

    Formatos_permitidos = ["text/csv", "text/plain"]
    Max_file_size = 10 * 1024 * 1024

    if not file.filename:
        raise HTTPException(status_code=400, detail="No se proporcionó un archivo válido")
    
    if file.content_type not in Formatos_permitidos:
        raise HTTPException(status_code=400, detail="No se proporcionó un archivo con un formato válido")

    if file.size > Max_file_size:
        raise HTTPException(status_code=413,detail="El archivo excede el tamaño máximo permitido de 10MB")

    await file.close()
    response = storage_service.upload_file_object(file.file, file.filename)

    return {
        "message": f"archivo '{file.filename}' se ha subido con exito",
        "content_type": file.content_type,
        "url": response
    }
