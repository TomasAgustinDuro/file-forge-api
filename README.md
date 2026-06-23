# 🔧 File Forge API

API de microservicios para la **gestión y carga de archivos** en un pipeline de datos. Construida con FastAPI y AWS S3, está diseñada con arquitectura orientada a servicios para escalar horizontalmente a medida que se agreguen nuevos microservicios.

---

## 📐 Arquitectura

```
Cliente HTTP
     │
     ▼
┌─────────────────────────────┐
│       services/uploader     │  ← FastAPI Microservicio
│                             │
│  POST /files/upload         │
│  GET  /status               │
│                             │
│  ┌──────────────────────┐   │
│  │   app/main.py        │   │  ← Capa de Transporte (rutas HTTP)
│  │   (endpoints)        │   │
│  └──────────┬───────────┘   │
│             │               │
│  ┌──────────▼───────────┐   │
│  │  app/services/       │   │  ← Capa de Servicios (lógica de negocio)
│  │  s3_storage.py       │   │
│  └──────────┬───────────┘   │
│             │               │
│  ┌──────────▼───────────┐   │
│  │   app/config.py      │   │  ← Configuración via variables de entorno
│  └──────────────────────┘   │
└─────────────────────────────┘
             │
             ▼
     ┌──────────────┐
     │   AWS S3     │  ← Almacenamiento de archivos
     └──────────────┘
```

---

## 🧩 Servicios

### `services/uploader`

Microservicio responsable de recibir archivos y almacenarlos en AWS S3.

| Endpoint | Método | Descripción |
|---|---|---|
| `/status` | GET | Health check — devuelve el estado del servicio y el entorno activo |
| `/files/upload` | POST | Recibe un archivo `multipart/form-data` y lo sube a S3 |

---

## ✅ Requisitos Previos

- **Python** 3.10 o superior
- **pip** o gestor de paquetes equivalente
- **Cuenta de AWS** con un bucket S3 configurado y credenciales con permisos de escritura (`s3:PutObject`)
- **AWS CLI** (opcional, útil para verificar credenciales)

---

## 🔐 Variables de Entorno

Crear un archivo `.env` dentro de `services/uploader/` basándose en la siguiente tabla:

| Variable | Descripción | Requerida | Valor por defecto |
|---|---|---|---|
| `APP_ENV` | Entorno de ejecución (`local`, `staging`, `production`) | No | `local` |
| `APP_PORT` | Puerto en el que corre el servidor | No | `8000` |
| `AWS_ACCESS_KEY_ID` | Access Key ID de AWS | **Sí** | — |
| `AWS_SECRET_ACCESS_KEY` | Secret Access Key de AWS | **Sí** | — |
| `AWS_DEFAULT_REGION` | Región de AWS donde está el bucket S3 | No | `us-east-1` |
| `AWS_S3_BUCKET` | Nombre del bucket S3 destino | **Sí** | — |

> ⚠️ **Nunca comitear el archivo `.env` al repositorio.** Está incluido en `.gitignore`.

---

## 🚀 Instalación y Configuración Local

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd file-forge-api
```

### 2. Crear y activar el entorno virtual

```bash
# Crear el entorno virtual
python -m venv .venv

# Activar en Windows (cmd)
.venv\Scripts\activate

# Activar en macOS/Linux
source .venv/bin/activate
```

### 3. Instalar dependencias del microservicio

```bash
cd services/uploader
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

```bash
# Dentro de services/uploader/
# Crear el archivo .env con las variables de la tabla anterior
copy .env.example .env   # Windows
cp .env.example .env     # macOS/Linux

# Editar .env y completar los valores requeridos
```

---

## ▶️ Cómo Correr el Servicio

Desde la carpeta `services/uploader/`:

```bash
uvicorn app.main:app --reload --port 8000
```

El servidor quedará disponible en `http://localhost:8000`.

La documentación interactiva (Swagger UI) se accede en:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 📡 Endpoints de la API

### `GET /status`

Verifica que el servicio esté funcionando. Devuelve el entorno y el bucket S3 configurado.

**Response `200 OK`:**
```json
{
  "status": "healthy",
  "environment": "local",
  "bucket_target": "mi-bucket-s3"
}
```

---

### `POST /files/upload`

Sube un archivo al bucket S3 configurado.

**Request:**
- Content-Type: `multipart/form-data`
- Campo: `file` — archivo a cargar

**Formatos aceptados:**
- `text/csv`
- `text/plain`

**Tamaño máximo:** 10 MB

**Response `200 OK`:**
```json
{
  "message": "archivo 'datos.csv' se ha subido con exito",
  "content_type": "text/csv",
  "url": "https://mi-bucket.s3.us-east-1.amazonaws.com/datos.csv"
}
```

**Errores posibles:**

| Código | Causa |
|---|---|
| `400` | No se proporcionó archivo o el formato es inválido |
| `413` | El archivo supera los 10 MB |
| `500` | Error interno al comunicarse con AWS S3 |

---

## ☁️ Despliegue en AWS

### Opción 1: EC2 / Servidor tradicional

1. Lanzar una instancia EC2 con Python 3.10+
2. Clonar el repositorio e instalar dependencias
3. Configurar las variables de entorno mediante AWS Systems Manager Parameter Store o un archivo `.env` seguro
4. Ejecutar con `uvicorn` detrás de un reverse proxy (Nginx o ALB)

### Opción 2: AWS Lambda + API Gateway (con Mangum)

1. Instalar `mangum` como adaptador ASGI: `pip install mangum`
2. Envolver la app con `Mangum(app)` en `main.py`
3. Empaquetar con todas las dependencias y subir a Lambda
4. Asignar un rol IAM con permisos `s3:PutObject` sobre el bucket destino
5. Configurar las variables de entorno en la consola de Lambda

### Consideraciones de IAM

El rol o usuario de AWS utilizado debe tener al menos la siguiente política:

```json
{
  "Effect": "Allow",
  "Action": ["s3:PutObject"],
  "Resource": "arn:aws:s3:::NOMBRE_DEL_BUCKET/*"
}
```

---

## 📁 Estructura del Proyecto

```
file-forge-api/
├── services/
│   └── uploader/                  # Microservicio de carga de archivos
│       ├── app/
│       │   ├── main.py            # Definición de la app FastAPI y endpoints
│       │   ├── config.py          # Configuración via pydantic-settings
│       │   └── services/
│       │       └── s3_storage.py  # Wrapper del cliente boto3 para S3
│       ├── requirements.txt       # Dependencias del microservicio
│       └── .env                   # Variables de entorno (no comitear)
├── .gitignore
└── README.md
```

---

## 📦 Dependencias

| Paquete | Versión | Uso |
|---|---|---|
| `fastapi` | 0.111.0 | Framework web principal |
| `uvicorn` | 0.30.1 | Servidor ASGI para correr FastAPI |
| `pydantic-settings` | 2.3.4 | Gestión de configuración desde variables de entorno |
| `boto3` | latest | SDK oficial de AWS para Python |

---

## 🔮 Roadmap

- [ ] Soporte para archivos `application/json`
- [ ] Validación del contenido del archivo (no solo el MIME type)
- [ ] Integración con SQS para notificar al pipeline cuando un archivo es cargado
- [ ] Autenticación de endpoints via API Key o JWT
- [ ] Soporte para subida multipart en chunks (archivos > 100 MB)
- [ ] Tests unitarios e integración con `pytest`

---

## 📄 Licencia

Este proyecto está bajo uso interno. Consultar con el equipo antes de redistribuir.
