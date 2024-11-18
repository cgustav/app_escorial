#!/bin/bash

cp .env.rds .env
docker-compose -f docker-compose.yml up web