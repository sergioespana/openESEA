#!/bin/bash

python3 manage.py collectstatic --no-input

gunicorn -t 300 -b 0.0.0.0:$PORT backend.wsgi
