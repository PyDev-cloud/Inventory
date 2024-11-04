from django.db import models
from django.contrib.auth. models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from .manager import BaseUser

# Create your models here.
Account_type={
    ("Staff","Staff"),
    ("Admin","Admin"),
    ("Employee","Employee"),
}

class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=60,unique=True)
    email=models.EmailField(max_length=100,validators=[UnicodeUsernameValidator,],unique=True)
    user_type=models.CharField(max_length=30,choices=Account_type,default="Staff")
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    join_date=models.DateTimeField(auto_now_add=True)

    objects=BaseUser()
    USERNAME_FIELD="username"
    REQUIRED_FIELDS=['email',]
    
    class Meta:
        ordering=["-join_date"]