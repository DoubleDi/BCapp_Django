# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bcapp', '0004_auto_20150527_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screenshot',
            name='is_avatar',
        ),
        migrations.AddField(
            model_name='bcuser',
            name='avatar',
            field=models.ImageField(upload_to=b'to/', null=True, verbose_name=b'avatar', blank=True),
            preserve_default=True,
        ),
    ]
