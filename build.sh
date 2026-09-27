#!/usr/bin/env bash
# Cloud build script for Render / Railway
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py seed_portfolio
