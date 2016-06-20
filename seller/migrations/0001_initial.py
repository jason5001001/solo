# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 16:35
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('address', models.CharField(max_length=100)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326, verbose_name='longitude/latitude')),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('radius', models.FloatField(default=10)),
                ('open_hour', models.TimeField(default='08:00:00')),
                ('close_hour', models.TimeField(default='18:30:00')),
                ('item', models.CharField(max_length=50)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6)),
                ('min_order', models.DecimalField(decimal_places=2, default=1.0, max_digits=6)),
                ('picture', models.FileField(blank=True, null=True, upload_to=b'')),
                ('description', models.TextField(blank=True, null=True)),
                ('min_order_amount', models.IntegerField(default=1)),
                ('permit_number', models.CharField(default='234523525342', max_length=50)),
                ('license', models.TextField(blank=True, null=True)),
                ('permit_exp', models.DateField(blank=True, null=True)),
                ('estimated_delivery', models.IntegerField(choices=[(1, '1 hour'), (2, 'Same Day'), (3, 'Next Day'), (4, 'Please Contact'), (5, 'Unknown')], default=1)),
                ('time_zone', models.CharField(blank=True, max_length=50, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('charge_id', models.CharField(blank=True, max_length=32, null=True)),
                ('delivery_address', models.CharField(max_length=500)),
                ('buyer_name', models.CharField(max_length=50)),
                ('buyer_phone', models.CharField(max_length=20)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WeekDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='seller',
            name='operating_days',
            field=models.ManyToManyField(related_name='operating_days', to='seller.WeekDay'),
        ),
        migrations.AddField(
            model_name='seller',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
