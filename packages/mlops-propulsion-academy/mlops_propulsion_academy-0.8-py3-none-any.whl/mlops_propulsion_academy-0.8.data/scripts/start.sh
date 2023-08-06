#!/usr/bin/env bash
source activate mlops
cd /mlops/backend
python manage.py migrate
python manage.py runserver 0:8000
