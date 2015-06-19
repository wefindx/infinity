# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150617_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='need',
            name='personal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]