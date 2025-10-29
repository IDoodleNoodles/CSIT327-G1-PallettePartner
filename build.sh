#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
npm ci
npm run build
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate