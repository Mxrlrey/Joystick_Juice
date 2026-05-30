#!/bin/sh
set -e

python manage.py migrate --noinput

python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if username and password:
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()

    try:
        from user.models import Person
        Person.objects.get_or_create(user=user)
    except Exception:
        pass

    print(f'Superuser {username} ready')

    client_id = os.environ.get('OAUTH_CLIENT_ID')
    client_secret = os.environ.get('OAUTH_CLIENT_SECRET')

    if client_id and client_secret:
        from oauth2_provider.models import get_application_model

        Application = get_application_model()
        app, created = Application.objects.get_or_create(
            client_id=client_id,
            defaults={
                'user': user,
                'client_type': Application.CLIENT_CONFIDENTIAL,
                'authorization_grant_type': Application.GRANT_PASSWORD,
                'name': 'Joystick Juice API',
            },
        )
        app.user = user
        app.client_type = Application.CLIENT_CONFIDENTIAL
        app.authorization_grant_type = Application.GRANT_PASSWORD
        app.name = 'Joystick Juice API'
        app.client_secret = client_secret
        app.save()
        print(f'OAuth application {client_id} ready')
else:
    print('DJANGO_SUPERUSER_USERNAME/PASSWORD not set; skipping superuser creation')
"

exec "$@"
