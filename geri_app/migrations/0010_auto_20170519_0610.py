# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 06:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geri_app', '0009_auto_20170519_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefactor',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]