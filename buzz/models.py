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
    image = CloudinaryField('image',default='https://res.cloudinary.com/marocho/image/upload/v1654523291/cld-sample-3.jpg')
    location = models.CharField(max_length=80, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user.username)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()


class Neighborhood(models.Model):
    name = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    population = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def create_neighborhood(self):
        self.save()

    def delete_neighborhood(self):
        self.delete()

    @classmethod
    def find_neighborhood(cls, search_term):
        results = cls.objects.filter(name__icontains=search_term)
        return results

    def update_neighborhood(self, name, location, population):
        self.name = name
        self.location = location
        self.population = population
        self.save()

    def get_population(self):
        return self.population

    def update_population(self, population):
        self.population = population
        self.save()

    def get_neighborhoods(self):
        return Neighborhood.objects.all()
    

    def __str__(self):
        return self.name


class Business(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email_address = models.EmailField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True)
    neighborhood = models.ForeignKey('Neighborhood',on_delete=models.CASCADE, blank=True)
    dated = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000)

    def create_business(self):
        self.save()

    def delete_business(self, business_name, business_email):
        self.name = business_name
        self.email = business_email
        self.delete()

    def update_business(self, business_name, business_email):
        self.name = business_name
        self.email = business_email
        self.save()

    @classmethod
    def find_business(cls, search_term):
        businesses = cls.objects.filter(name__icontains=search_term)
        return businesses

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70, blank=True)
    description = models.CharField(max_length=500, blank=True)
    content = models.TextField(blank=True)
    image = CloudinaryField('image',null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_on',)

    @classmethod
    def search_post(cls, search_term):
        results = cls.objects.filter(name__icontains=search_term)
        return results
