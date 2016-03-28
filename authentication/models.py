# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from time import time
from wease import settings
from django.core.files.storage import default_storage
from django.utils.encoding import smart_unicode

def get_upload_file_name(instance, filename):
    return settings.UPLOAD_FILE_PATTERN % (str(time()).replace('.','_'), filename)

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username'),
            first_name=kwargs.get('first_name'), last_name=kwargs.get('last_name'),
            )
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_admin = True
        account.save()

        return account

class Account(AbstractBaseUser):
    lang_def = 'fr'

    SUPER = '9'
    ADMIN = '8'
    MANAGER = '7'
    APPROVE = '6'
    SUBMIT = '5'
    VIEW = '2'
    ACCESS_LEVEL = ( 
        (SUPER, 'Super'),
        (ADMIN, 'Administrator'),
        (MANAGER, 'Manager'),
        (APPROVE, 'Approve'),
        (SUBMIT, 'Submit'),
        (VIEW, 'View'),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    tagline = models.CharField(max_length=140, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    optiz = models.BooleanField(default=False)
    lang = models.CharField(max_length=3, null=True, blank=True, default=lang_def.lower())
    user_company = models.ForeignKey('Company', null=True, blank=True, related_name='wease_company')
    position = models.CharField(max_length=120, null=True, blank=True)
    access_level = models.CharField(max_length=2, choices=ACCESS_LEVEL, default=VIEW)
    auth_amount = models.CharField(max_length=7, null=True, blank=True, default=0)
    street_addr1 = models.CharField(max_length=50, null=True, blank=True)
    street_addr2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    post_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)    
    phone_main = models.CharField(max_length=30, null=True, blank=True)
    phone_mobile = models.CharField(max_length=30, null=True, blank=True)
    user_pic = models.FileField(upload_to=get_upload_file_name, null=True, blank=True, default='uploads/blank_user.png')
    user_created = models.DateTimeField(auto_now_add=True)
    user_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_user', null=True, blank=True, unique=False)
    user_updated = models.DateTimeField(auto_now=True)
    user_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_user', null=True, blank=True, unique=False)
    request_email = models.BooleanField(default=True)
    offer_email = models.BooleanField(default=True)
    order_email = models.BooleanField(default=True)
    approval_email = models.BooleanField(default=True)
    validated_email = models.BooleanField(default=True)
    refused_email = models.BooleanField(default=True)
    canceled_email = models.BooleanField(default=True)
    new_user_email = models.BooleanField(default=True)
    info_change_email = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin   


class Company(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    company_address = models.ForeignKey('Address', null=True, blank=True, related_name='default_address')    
    company_logo = models.FileField(upload_to=get_upload_file_name, null=True, blank=True, default='uploads/blank_co.png')
    company_website = models.CharField(max_length=200, null=True, blank=True)
    company_created = models.DateTimeField(auto_now_add=True)    
    company_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_company', unique=False)
    company_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    company_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_company', null=True, blank=True, unique=False)
    company_assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_to', limit_choices_to={'optiz': True}, blank=True)

    def __unicode__(self):
      return smart_unicode(self.name)

    def get_name(self):
        return smart_unicode(self.name)

class Address(models.Model):
    OFFICE = 'OFF'
    DELIVERY = 'DEL'
    OTHER = 'OTH'
    ADDR_LOC = ( 
        (OFFICE, 'Office'),
        (DELIVERY, 'Delivery'),
        (OTHER, 'Other'),
    )    
    addr_default = models.BooleanField(default=False)
    addr_type = models.CharField(max_length=3, choices=ADDR_LOC, default=OFFICE)
    addr_location = models.CharField(max_length=50, null=True, blank=True)
    addr_company = models.ForeignKey(Company, related_name='address_company', null=True, blank=True)
    addr_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='address_user', null=True, blank=True)
    street_addr1 = models.CharField(max_length=50, null=True, blank=True)
    street_addr2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    post_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    phone_main = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    addr_notes = models.TextField(null=True, blank=True)
    addr_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='address_created_user')
    addr_created_date = models.DateTimeField(auto_now_add=True)
    addr_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='address_updated_user')
    addr_updated_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.addr_company:
            return self.addr_company.name
        else:
            return self.addr_user.username    
    

