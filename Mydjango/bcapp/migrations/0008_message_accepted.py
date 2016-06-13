# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bcapp', '0007_auto_20150606_0219'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='accepted',
            field=models.CharField(max_length=30, null=True, verbose_name=b'accepted', blank=True),
            preserve_default=True,
        ),
    ]
