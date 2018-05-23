# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-23 20:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('friendship', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts_by', to='account.Profile'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts_to', to='account.Profile'),
        ),
    ]
