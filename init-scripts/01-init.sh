# init-scripts/01-init.sh
#!/bin/bash
echo "Esperando que MySQL esté listo..."
while ! mysqladmin ping -h"localhost" --silent; do
    sleep 1
done

echo "MySQL está listo, importando datos..."
mysql -u root -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE" < /docker-entrypoint-initdb.d/bulk_data.sql
echo "Importación completada"