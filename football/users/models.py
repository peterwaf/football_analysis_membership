from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_('Email Address'),unique= True)
    username = models.CharField(_('Username'),unique= True, max_length=50)
    first_name = models.CharField(_('First Name'),blank=True,max_length=50)
    last_name = models.CharField(_('Last Name'),blank=True,max_length=50)
    mobile_number = models.CharField(_('Mobile Number'),blank=True,max_length=50)
    is_staff = models.BooleanField(_('IS STAFF '),default=False)
    is_active = models.BooleanField(default=True)
    subscribed = models.BooleanField(default=False)
    subscription_start = models.DateTimeField(blank=True,null=True)
    subscription_end = models.DateTimeField(blank=True,null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    #ask for email instead of the default username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('email',)
    objects = CustomUserManager()
    # helper functions
    # eg creating user functions/retrieving user & permissions

    def __str__(self):
        return self.email
        
    class Meta:
        verbose_name_plural = 'Users'