# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bcapp', '0005_auto_20150528_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bcuser',
            name='karma',
        ),
        migrations.RemoveField(
            model_name='databasemonster',
            name='karma',
        ),
    ]
