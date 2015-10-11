# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import authentication.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('username', models.CharField(unique=True, max_length=40)),
                ('first_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=50, blank=True)),
                ('tagline', models.CharField(max_length=140, null=True, blank=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('optiz', models.BooleanField(default=False)),
                ('lang', models.CharField(default=b'fr', max_length=3, null=True, blank=True)),
                ('position', models.CharField(max_length=120, null=True, blank=True)),
                ('access_level', models.CharField(default=b'2', max_length=2, choices=[(b'9', b'Super'), (b'8', b'Administrator'), (b'7', b'Manager'), (b'6', b'Approve'), (b'5', b'Submit'), (b'2', b'View')])),
                ('auth_amount', models.CharField(default=0, max_length=7, null=True, blank=True)),
                ('street_addr1', models.CharField(max_length=50, null=True, blank=True)),
                ('street_addr2', models.CharField(max_length=50, null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('post_code', models.CharField(max_length=10, null=True, blank=True)),
                ('country', models.CharField(max_length=50, null=True, blank=True)),
                ('phone_main', models.CharField(max_length=30, null=True, blank=True)),
                ('phone_mobile', models.CharField(max_length=30, null=True, blank=True)),
                ('user_pic', models.FileField(default=b'uploads/blank_user.png', null=True, upload_to=authentication.models.get_upload_file_name, blank=True)),
                ('user_created', models.DateTimeField(auto_now_add=True)),
                ('user_updated', models.DateTimeField(auto_now=True)),
                ('request_email', models.BooleanField(default=True)),
                ('offer_email', models.BooleanField(default=True)),
                ('order_email', models.BooleanField(default=True)),
                ('approval_email', models.BooleanField(default=True)),
                ('validated_email', models.BooleanField(default=True)),
                ('refused_email', models.BooleanField(default=True)),
                ('canceled_email', models.BooleanField(default=True)),
                ('new_user_email', models.BooleanField(default=True)),
                ('info_change_email', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('addr_default', models.BooleanField(default=False)),
                ('addr_type', models.CharField(default=b'OFF', max_length=3, choices=[(b'OFF', b'Office'), (b'DEL', b'Delivery'), (b'OTH', b'Other')])),
                ('addr_location', models.CharField(max_length=50, null=True, blank=True)),
                ('street_addr1', models.CharField(max_length=50, null=True, blank=True)),
                ('street_addr2', models.CharField(max_length=50, null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('post_code', models.CharField(max_length=10, null=True, blank=True)),
                ('country', models.CharField(max_length=50, null=True, blank=True)),
                ('phone_main', models.CharField(max_length=30, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('addr_notes', models.TextField(null=True, blank=True)),
                ('addr_created_date', models.DateTimeField(auto_now_add=True)),
                ('addr_updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('company_logo', models.FileField(default=b'uploads/blank_co.png', null=True, upload_to=authentication.models.get_upload_file_name, blank=True)),
                ('company_website', models.CharField(max_length=200, null=True, blank=True)),
                ('company_created', models.DateTimeField(auto_now_add=True)),
                ('company_updated', models.DateTimeField(auto_now=True)),
                ('company_address', models.ForeignKey(related_name='default_address', blank=True, to='authentication.Address', null=True)),
                ('company_assigned_to', models.ManyToManyField(related_name='assigned_to', to=settings.AUTH_USER_MODEL, blank=True)),
                ('company_created_by', models.ForeignKey(related_name='created_company', to=settings.AUTH_USER_MODEL)),
                ('company_updated_by', models.ForeignKey(related_name='updated_company', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='addr_company',
            field=models.ForeignKey(related_name='address_company', blank=True, to='authentication.Company', null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='addr_created_by',
            field=models.ForeignKey(related_name='address_created_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='address',
            name='addr_updated_by',
            field=models.ForeignKey(related_name='address_updated_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='addr_user',
            field=models.ForeignKey(related_name='address_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='user_company',
            field=models.ForeignKey(related_name='wease_company', blank=True, to='authentication.Company', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='user_created_by',
            field=models.ForeignKey(related_name='created_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='user_updated_by',
            field=models.ForeignKey(related_name='updated_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
