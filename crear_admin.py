import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings_prod")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("ADMIN_USERNAME")
email = os.environ.get("ADMIN_EMAIL")
password = os.environ.get("ADMIN_PASSWORD")

if username and email and password:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email},
    )

    user.email = email
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()

    print("Superusuario configurado correctamente.")
else:
    print("Variables de administrador no configuradas.")