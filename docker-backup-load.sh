#!/bin/bash

docker-compose exec -T db mysql -u root -p"root_password" django_db < backup.sql