#!/bin/sh

# Setup environment variables
export ALGATOR_ROOT='/ALGATOR_ROOT'
export DJANGO_SETTINGS_MODULE='ALGator.settings'

gunicorn ALGator.wsgi:application \
--timeout 5 \
--bind 0.0.0.0:8000 
