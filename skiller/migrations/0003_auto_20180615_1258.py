# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-15 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skiller', '0002_auto_20180607_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skilldata',
            name='_codename',
            field=models.CharField(db_column='skill name', help_text='codename for the skill', max_length=20, unique=True),
        ),
    ]