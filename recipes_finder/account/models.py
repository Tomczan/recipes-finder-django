from django.db import models
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    nickname = models.TextField(max_length=150)
    photo = models.ImageField(blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
