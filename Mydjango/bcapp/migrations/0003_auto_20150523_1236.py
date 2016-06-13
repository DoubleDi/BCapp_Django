# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bcapp', '0002_auto_20150523_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screenshot',
            name='picture',
            field=models.ImageField(upload_to=b'to/', verbose_name=b'picture', blank=True),
        ),
    ]
