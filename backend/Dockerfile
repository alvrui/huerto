# Usar imagen oficial de Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar requisitos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY ./src /app/src

# Exponer puerto de FastAPI
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
