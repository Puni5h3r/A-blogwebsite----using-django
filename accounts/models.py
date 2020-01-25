from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin, AbstractBaseUser
from mysite.settings import DATE_INPUT_FORMATS
# Create your models here.
class User(AbstractUser):
    pass
    #REQUIRED_FIELDS = ['date_of_birth', 'height']

    def __str__(self):
        return "@{}".format(self.username)
