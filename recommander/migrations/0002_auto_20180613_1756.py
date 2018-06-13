# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-13 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommander', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(choices=[('v', 'user visited'), ('s', 'has confirmed skill')], max_length=1),
        ),
    ]