# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publicweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='resolved',
            field=models.BooleanField(default=False, verbose_name='Resolved'),
            preserve_default=True,
        ),
    ]
