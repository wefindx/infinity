# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-28 00:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20160218_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='definition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Definition'),
        ),
    ]
