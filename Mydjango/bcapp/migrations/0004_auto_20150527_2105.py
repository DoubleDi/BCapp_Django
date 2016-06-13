# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bcapp', '0003_auto_20150523_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='databasemonster',
            name='picture',
            field=models.ImageField(upload_to=b'to/', verbose_name=b'picture', blank=True),
        ),
        migrations.AlterField(
            model_name='monster',
            name='picture',
            field=models.ImageField(upload_to=b'to/', verbose_name=b'picture', blank=True),
        ),
    ]
