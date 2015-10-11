# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import authentication.models
import swampdragon.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('users', models.ManyToManyField(related_name='chat_users', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chat_message_created', models.DateTimeField(auto_now_add=True)),
                ('chat_message', models.TextField(null=True, blank=True)),
                ('chat', models.ForeignKey(related_name='chat_group', to='messaging.Chat')),
                ('chat_viewed', models.ManyToManyField(related_name='chat_viewed', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='chat_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-chat_message_created'],
            },
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=250, null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('mail_draft', models.BooleanField(default=False)),
                ('mail_read', models.BooleanField(default=False)),
                ('mail_created', models.DateTimeField(auto_now_add=True)),
                ('mail_created_by', models.ForeignKey(related_name='mail_created_by_user', to=settings.AUTH_USER_MODEL)),
                ('mail_read_by', models.ManyToManyField(related_name='mail_read_by', to=settings.AUTH_USER_MODEL, blank=True)),
                ('mail_to', models.ManyToManyField(related_name='mail_sent_to', to=settings.AUTH_USER_MODEL, blank=True)),
                ('trash', models.ManyToManyField(related_name='mail_trash_by', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
        migrations.CreateModel(
            name='MailFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_created', models.DateTimeField(auto_now=True)),
                ('mail_file', models.FileField(null=True, upload_to=authentication.models.get_upload_file_name, blank=True)),
                ('base_mail', models.ForeignKey(related_name='base_files', blank=True, to='messaging.Mail', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MailReply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=250, null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('reply_draft', models.BooleanField(default=False)),
                ('reply_created', models.DateTimeField(auto_now_add=True)),
                ('mail_to', models.ManyToManyField(related_name='reply_sent_to', to=settings.AUTH_USER_MODEL, blank=True)),
                ('orig_mail', models.ForeignKey(related_name='reply_mail', to='messaging.Mail')),
                ('reply_created_by', models.ForeignKey(related_name='reply_created_by_user', to=settings.AUTH_USER_MODEL)),
                ('reply_read_by', models.ManyToManyField(related_name='reply_read_by', to=settings.AUTH_USER_MODEL, blank=True)),
                ('trash', models.ManyToManyField(related_name='reply_trash_by', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
        migrations.AddField(
            model_name='mailfile',
            name='reply_mail',
            field=models.ForeignKey(related_name='reply_files', blank=True, to='messaging.MailReply', null=True),
        ),
    ]
