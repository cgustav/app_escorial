#!/bin/bash

# Detener los contenedores
docker-compose down
# Eliminar el contenedor de la base de datos (pero no el volumen)
docker volume rm mysql_persistent_data
docker volume create mysql_persistent_data
# Reiniciar los contenedores
docker-compose up -d