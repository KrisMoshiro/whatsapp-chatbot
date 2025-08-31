# Imagen base ligera
FROM python:3.11-slim

# Evita .pyc y mejora logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*

# Instalar deps de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Asegurar que 'src' se pueda importar como paquete
ENV PYTHONPATH=/app

# Cloud Run usa $PORT (exponer es opcional pero claro)
EXPOSE 8080

# Ejecutar con gunicorn el objeto WSGI "application" definido en application.py
CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 application:application