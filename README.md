# Configuración de Entornos

## Desarrollo Local

```bash
# Iniciar entorno local con MySQL en Docker
./start-local.sh
```

## Desarrollo con RDS

```bash
# Configurar variables de entorno
cp .env.rds.example .env.rds
# Editar .env.rds con las credenciales correctas

# Iniciar aplicación conectada a RDS
./start-rds.sh
```

## Migraciones

```bash
# Migraciones en local
docker-compose run --rm web python manage.py migrate

# Migraciones en RDS
./migrate-rds.sh
```

## Carga de Datos

```bash
# Cargar datos en local
docker-compose up db
# Esperar a que MySQL esté listo

# Cargar datos en RDS
./load-data-rds.sh
```
