#!/bin/bash

# Ver logs de la importación
# docker-compose logs db

docker-compose exec db mysqldump -u root -p"root_password" django_db > backup.sql