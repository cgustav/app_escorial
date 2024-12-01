#!/bin/sh
# Esperar a que la base de datos esté lista
python manage.py wait_for_db

# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Iniciar el servidor
python manage.py runserver 0.0.0.0:8000