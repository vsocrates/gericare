# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-11 05:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geri_app', '0004_auto_20170411_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefactor',
            name='patientCheckedOutDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
