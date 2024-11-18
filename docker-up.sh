#!/bin/bash

docker volume create mysql_persistent_data

# Copia el contenido del script 01-init.sh mostrado arriba
chmod +x init-scripts/01-init.sh

docker-compose up -d

# Ver logs de la importación
docker-compose logs db

# Conectarse a MySQL para verificar los datos
docker-compose exec db mysql -u django_user -pdjango_password django_db