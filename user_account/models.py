from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    # email = models.EmailField(unique=True,default=None)
    # is_active = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.username
