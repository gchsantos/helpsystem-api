#!/usr/bin/env sh

NAME="helpsystem_api"

if ! python manage.py test --k; then
    echo '[ ALERT: Application not pass in the tests. ]'
    exit 1
fi

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000