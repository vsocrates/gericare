# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-09 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geri_app', '0012_benefactor_relation'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediadocument',
            name='hasBeenViewed',
            field=models.BooleanField(default=False),
        ),
    ]
