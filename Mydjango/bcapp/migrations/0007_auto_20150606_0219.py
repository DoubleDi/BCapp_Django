# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bcapp', '0006_auto_20150605_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='owner',
            field=models.ForeignKey(related_name=b'to_monster', verbose_name=b'to_monster', to='bcapp.Monster'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(related_name=b'from_monster', verbose_name=b'from_monster', to='bcapp.Monster'),
        ),
    ]
