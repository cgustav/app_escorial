#!/bin/bash

mysql -h $RDS_ENDPOINT -u administrador -p el_escorial < bulk_data.sql

