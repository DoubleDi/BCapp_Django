# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bcapp', '0008_message_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='bcuser',
            name='view',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='view',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
