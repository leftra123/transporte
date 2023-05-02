# Use una imagen oficial de Python como base
FROM python:3.9

# Establece la variable de entorno para que Python use utf-8
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias del proyecto
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del proyecto
COPY . /app/

# Expone el puerto en el que se ejecutará el servidor
EXPOSE 8000

# Ejecuta el servidor de Django
CMD ["gunicorn", "colegio_transportes.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
