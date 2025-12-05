from django.db import models
from joystickjuice.utils import GENDER_OPTIONS 
from django.conf import settings

# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='person')
    name = models.CharField("Nome", max_length=100, null=True, blank=True)
    birthdate = models.DateField("Data de nascimento", null=True, blank=True)
    gender = models.CharField("Sexo", max_length=1, choices=GENDER_OPTIONS, null=True, blank=True)
    avatar_url = models.ImageField("Avatar", upload_to='perfil/', null=True, blank=True)
    bio = models.CharField("Biografia", max_length=200, null=True, blank=True)

    