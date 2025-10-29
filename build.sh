#!/usr/bin/env bash
set -o errexit

python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate