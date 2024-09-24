#!/bin/bash

# Activa el entorno virtual
source pyvenv/bin/activate


python3 -m pip install -r requirements.txt
# Realiza las migraciones
python manage.py migrate


python3 manage.py collectstatic --noinput

