# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-12 18:06
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('active', models.CharField(choices=[('Active', 'Active'), ('Not Active', 'Not Active')], default='Not Active', max_length=20)),
                ('phone_number', models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('radius', models.IntegerField(default=10)),
                ('fulfillment_partner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('email', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326, verbose_name='longitude/latitude')),
                ('radius', models.IntegerField(default=10)),
                ('open_hour', models.IntegerField()),
                ('close_hour', models.IntegerField()),
                ('item', models.CharField(max_length=50)),
                ('item_unit', models.CharField(max_length=50)),
                ('price_unit', models.CharField(max_length=50)),
                ('picture', models.FileField(upload_to=b'')),
                ('description', models.TextField()),
                ('min_order_amount', models.IntegerField()),
                ('license', models.TextField()),
                ('license_exp', models.DateField()),
                ('is_active', models.BooleanField()),
                ('operating_days', models.CharField(max_length=100)),
            ],
            managers=[
                ('gis', django.db.models.manager.Manager()),
            ],
        ),
    ]
