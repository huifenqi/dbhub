# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-12 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0009_database_enable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='enable',
            field=models.NullBooleanField(choices=[(True, 'on'), (False, 'off')], default=False, help_text='\u662f\u5426\u542f\u7528'),
        ),
    ]