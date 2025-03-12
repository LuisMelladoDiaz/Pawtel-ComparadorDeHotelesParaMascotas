#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

python manage.py migrate

if [ $# -eq 1 ] && [ "$1" == "--seed" ]; then
    python manage.py seed --clear
fi
