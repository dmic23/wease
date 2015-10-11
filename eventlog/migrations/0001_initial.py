# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import swampdragon.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('not_action', models.CharField(max_length=50, db_index=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('notification', models.BooleanField(default=False)),
                ('extra', jsonfield.fields.JSONField(default=dict)),
                ('company', models.ForeignKey(blank=True, to='authentication.Company', null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('viewed_by', models.ManyToManyField(related_name='user_viewed', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
    ]
