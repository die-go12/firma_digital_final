#imagen base ligera de python
FROM python:3.10-slim

# evitamos generar archivos temporales
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# directorio
WORKDIR /app

# instalamos dependencias necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# copiamos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copiamos todo
COPY . .

# creamos las carpetas de almacenamiento 
RUN mkdir -p storage/keys storage/certs storage/signed_pdfs storage/temp

# exponemos el puerto 8000 
EXPOSE 8000

# comando para iniciar
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]