# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150615_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True),
        ),
    ]