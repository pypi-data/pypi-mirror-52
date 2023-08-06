#!/usr/bin/env bash
source activate mlops
cd /mlops
export DJANGO_DEBUG=0
docker-compose up -d
cd /mlops/backend
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0:8000
