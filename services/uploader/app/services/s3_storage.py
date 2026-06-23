import boto3
import logging
from botocore.exceptions import ClientError
from fastapi import HTTPException
from app.config import settings


class S3StorageService:
    def __init__(self):
        self.botoClient = boto3.client(
            "s3",
            region_name=settings.aws_default_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

    def upload_file_object(self, file_object, object_name: str):
        """
        Recibe el file.file de FastAPI y lo transmite a S3.
        Devuelve la URL del archivo o un mensaje de éxito
        """

        try:
            self.botoClient.upload_fileobj(file_object, settings.aws_s3_bucket, object_name)

            return f"https://{settings.aws_s3_bucket}.s3.{settings.aws_default_region}.amazonaws.com/{object_name}" 
        except ClientError as e:
            logging.error(e)
            raise HTTPException(status_code=500, detail="Error interno al cargar el archivo en el almacenamiento en la nube.")
            
