# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publicweb', '0002_auto_20150312_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationsettings',
            name='notification_level',
            field=models.IntegerField(default=3, help_text='Levels are cumulative, so if, for example, you choose to get notifications of replies to feedback, you will get notifications of all changes to main items as well.', verbose_name='Notification level', choices=[(0, '1. Silent'), (1, '2. Major events'), (2, '3. Feedback and changes'), (3, '4. Full discussion'), (4, '5. Everything, even minor changes')]),
            preserve_default=True,
        ),
    ]
