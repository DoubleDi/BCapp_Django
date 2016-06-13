# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bcapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='databasemonster',
            name='picture',
            field=models.ImageField(upload_to=b'/home/doubledi/Documents/django/Mydjango/generatefiles/media/to', verbose_name=b'picture', blank=True),
        ),
    ]
