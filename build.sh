#!/usr/bin/env bash

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "
from apps.user.models import User
if not User.objects.filter(email='admin@compia.com').exists():
    User.objects.create_superuser(email='admin@compia.com', password='admin@123', nome='Admin', role='BACKOFFICE')
"