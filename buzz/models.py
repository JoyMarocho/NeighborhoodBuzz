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

def create_staffuser(self,email,password,**extra_fields):
        """
            Create and save a Staff User with the given email and password.
        """
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
    
        if extra_fields.get('is_staff') is not True:
            raise ValueError('SUpdateUserFormtaff user must have is_staff=True.')
        return self.create_user(email, password, **extra_fields)

def create_superuser(self,email,password=None,**extra_fields):
        """
            Create and save a SuperUser with the given email and password.
        """
    #extra_fields.setdefault('is_staff', True)
    #extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active', True)

        # if extra_fields.get('is_staff') is not True:
            #   raise ValueError('Superuser must have is_staff=True.')
        # if extra_fields.get('is_superuser')is not True:
            #   raise ValueError('Superuser must have superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
        identification_number = models.IntegerField(default=1)
        email = models.EmailField(verbose_name='email address', unique=True)
        neighborhood = models.ForeignKey('Neighborhood', on_delete=models.CASCADE, null=True, blank=True)
        
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)
        is_superuser = models.BooleanField(default=False)

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []

        objects = UserManager()

        def __str__(self):
            return self.email

        def get_full_name(self):
            return self.email

        def get_username(self):
            return self.email

        def has_perm(self,perm,obj=None):
            return True

    # @property
    # def is_staff(self):
    #   return self.is_staff

    # @property
    # def is_superuser(self):
    #   return self.is_superuser 

class Profile(models.Model):
        user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True)
        bio = models.TextField(max_length=200, blank=True)
        image = CloudinaryField('image', blank=True)
        location = models.CharField(max_length=80, blank=True)
        date_joined = models.DateTimeField(default=timezone.now)

        def __str__(self):
            return str(self.user.username)

        def save_profile(self):
            self.save()

        def delete_profile(self):
            self.delete()

class Neighborhood(models.Model):
        name = models.CharField(max_length=80, blank=True)
        location = models.CharField(max_length=80, blank=True)
        population = models.IntegerField(blank=True)

        def __str__(self):
            return self.name

