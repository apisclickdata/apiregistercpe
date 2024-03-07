# Establece la imagen base de Python con App Runner
FROM python:3.9.7

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y default-jre-headless wget


WORKDIR /app
# Copia el contenido del directorio actual al directorio de trabajo en el contenedor
COPY . /app

# Define la ubicación del entorno virtual
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Instala virtualenv y crea el entorno virtual
RUN pip install --no-cache-dir virtualenv && \
    virtualenv $VIRTUAL_ENV

# Activa el entorno virtual y establece el directorio de trabajo en el contenedor
WORKDIR /app
RUN echo "source /app/venv/bin/activate" >> /root/.bashrc

# Instala las dependencias del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Inicia el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
