# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('created_by', models.ForeignKey(related_name='wease_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('good_info', models.CharField(max_length=200, null=True, blank=True)),
                ('good_description', models.CharField(max_length=250, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=50, null=True, blank=True)),
                ('family', models.CharField(max_length=50, null=True, blank=True)),
                ('subfamily', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('offer_version', models.SmallIntegerField(null=True, blank=True)),
                ('offer_domain', models.CharField(max_length=250, null=True, blank=True)),
                ('offer_total', models.CharField(max_length=50, null=True, blank=True)),
                ('offer_terms', models.TextField(null=True, blank=True)),
                ('offer_created', models.DateTimeField(auto_now_add=True)),
                ('offer_approval_status', models.CharField(default=b'WAP', max_length=3, choices=[(b'REF', b'Refus\xc3\xa9'), (b'APV', b'Approuv\xc3\xa9'), (b'WAP', b'Waiting Approval')])),
                ('offer_approval', models.DateTimeField(null=True, blank=True)),
                ('offer_approval_by', models.ForeignKey(related_name='offer_updated_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('offer_created_by', models.ForeignKey(related_name='offer_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OfferItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_name', models.CharField(max_length=250, null=True, blank=True)),
                ('item_details', models.TextField(null=True, blank=True)),
                ('price', models.CharField(max_length=50, null=True, blank=True)),
                ('item_sub_total', models.CharField(max_length=50, null=True, blank=True)),
                ('frequency', models.CharField(max_length=50, null=True, blank=True)),
                ('quantity', models.SmallIntegerField(null=True, blank=True)),
                ('delivery_date', models.DateTimeField(max_length=50, null=True, blank=True)),
                ('date_start', models.DateTimeField(null=True, blank=True)),
                ('date_end', models.DateTimeField(null=True, blank=True)),
                ('offer', models.ForeignKey(related_name='offer_item', to='orders.Offer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_draft', models.BooleanField(default=False)),
                ('order_number', models.CharField(max_length=50, null=True, blank=True)),
                ('order_version', models.SmallIntegerField(null=True, blank=True)),
                ('offer_version', models.SmallIntegerField(default=0, null=True, blank=True)),
                ('order_offer', models.BooleanField(default=False)),
                ('reference_number', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('order_total', models.CharField(max_length=50, null=True, blank=True)),
                ('order_created', models.DateTimeField(auto_now_add=True)),
                ('modified_by_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('order_status', models.CharField(default=b'WRQ', max_length=3, choices=[(b'WRQ', b'Demandes en attente'), (b'PEN', b'Demandes \xc3\xa0 traiter'), (b'OFR', b'Offre disponible'), (b'VAL', b'Commande \xc3\xa0 traiter'), (b'REF', b'Refus\xc3\xa9'), (b'APV', b'Approuv\xc3\xa9'), (b'COM', b'Completed'), (b'INV', b'Invoiced'), (b'CAN', b'Annul\xc3\xa9'), (b'ARC', b'Archived'), (b'RSB', b'Request Submitted'), (b'APN', b'Approval Needed'), (b'OSB', b'Optiz Offer Submitted'), (b'NAP', b'Not Approved'), (b'RET', b'Returned'), (b'INP', b'In Progress'), (b'BOR', b'Backorder')])),
                ('order_status_change_date', models.DateTimeField(null=True, blank=True)),
                ('company_approval_status', models.CharField(default=b'PEN', max_length=3, choices=[(b'WRQ', b'Demande en attente'), (b'PEN', b'Demande en cours de traitement'), (b'OFR', b'Offre disponible'), (b'VAL', b'Commande valid\xc3\xa9e'), (b'REF', b'Refus\xc3\xa9'), (b'APV', b'Approuv\xc3\xa9'), (b'COM', b'Commande finalis\xc3\xa9e'), (b'INV', b'Invoiced'), (b'CAN', b'Annul\xc3\xa9'), (b'ARC', b'Archived'), (b'RSB', b'Request Submitted'), (b'APR', b'Request Approved'), (b'APN', b'Approval Needed'), (b'APO', b'Offer Approved'), (b'NAP', b'Not Approved'), (b'RET', b'Returned')])),
                ('company_approval_date', models.DateTimeField(null=True, blank=True)),
                ('optiz_status', models.CharField(default=b'PEN', max_length=3, choices=[(b'WRQ', b'Demande en attente'), (b'PEN', b'Demande \xc3\xa0 traiter'), (b'OFR', b'Offre disponible'), (b'VAL', b'Commande \xc3\xa0 traiter'), (b'REF', b'Refus\xc3\xa9'), (b'APV', b'Approuv\xc3\xa9'), (b'COM', b'Commandes \xc3\xa0 facturer'), (b'INV', b'Invoiced'), (b'CAN', b'Annul\xc3\xa9'), (b'ARC', b'Archived'), (b'OSB', b'Offer Submitted'), (b'NAP', b'Not Approved'), (b'RET', b'Returned'), (b'INP', b'In Progress'), (b'BOR', b'Backorder')])),
                ('optiz_status_change_date', models.DateTimeField(null=True, blank=True)),
                ('company_approval_by', models.ForeignKey(related_name='order_approved_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('delivery_address', models.ForeignKey(related_name='company_address', blank=True, to='authentication.Address', null=True)),
                ('modified_by', models.ForeignKey(related_name='order_modified_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('optiz_status_change_by', models.ForeignKey(related_name='optiz_approved_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('order_company', models.ForeignKey(related_name='order_company', blank=True, to='authentication.Company', null=True)),
                ('order_created_by', models.ForeignKey(related_name='order_created_user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('order_status_change_by', models.ForeignKey(related_name='order_status_changed_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReqFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_created', models.DateTimeField(auto_now=True)),
                ('req_file', models.FileField(null=True, upload_to=orders.models.get_upload_file_name, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReqItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('req_domain', models.CharField(max_length=250, null=True, blank=True)),
                ('item_fam', models.CharField(max_length=250, null=True, blank=True)),
                ('item_subfam', models.CharField(max_length=250, null=True, blank=True)),
                ('item_details', models.TextField(null=True, blank=True)),
                ('req_item_created', models.DateTimeField(auto_now_add=True)),
                ('req_item_modified', models.DateTimeField(auto_now=True)),
                ('good', models.ForeignKey(related_name='req_good', to='orders.Good')),
                ('order', models.ForeignKey(related_name='req_order', to='orders.Order')),
                ('req_item_created_by', models.ForeignKey(related_name='req_item_modified_user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('req_item_modified_by', models.ForeignKey(related_name='req_item_created_user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReqProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prod_fam', models.CharField(max_length=250, null=True, blank=True)),
                ('prod_subfam', models.CharField(max_length=250, null=True, blank=True)),
                ('prod_title', models.CharField(max_length=250, null=True, blank=True)),
                ('prod_details', models.CharField(default=b'NONE', max_length=250, null=True, blank=True)),
                ('prod_description', models.CharField(max_length=250, null=True, blank=True)),
                ('req_item', models.ForeignKey(related_name='req_product', to='orders.ReqItem')),
            ],
        ),
        migrations.AddField(
            model_name='reqfile',
            name='req_item',
            field=models.ForeignKey(related_name='req_item_file', blank=True, to='orders.ReqItem', null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='order',
            field=models.ForeignKey(related_name='offer_order', to='orders.Order'),
        ),
        migrations.AddField(
            model_name='detail',
            name='good',
            field=models.ForeignKey(related_name='good_detail', to='orders.Good'),
        ),
        migrations.AddField(
            model_name='comment',
            name='order',
            field=models.ForeignKey(related_name='order_comment', to='orders.Order'),
        ),
    ]
