# Dockerfile para Django
FROM python:3.9

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY dependencias.txt .
RUN pip install -r dependencias.txt
RUN pip3 install psycopg2-binary python-dotenv

# Copiar el proyecto
COPY . .

# Puerto que expondrá Django
EXPOSE 8000

# Comando para ejecutar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

