from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



# Create your models here.
class UserManager(BaseUserManager):
    """
        Custom user model manager where email is the unique identifiers
        for authentication instead of usernames.
    """
    def create_user(self,email, password=None, **extra_fields):
    
        """
            Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('User must have a valid username')
    #extra_fields.setdefault('is_superuser',False)
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        