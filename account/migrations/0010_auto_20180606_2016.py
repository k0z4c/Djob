# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-06 20:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20180606_1729'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='img',
            new_name='_img',
        ),
    ]