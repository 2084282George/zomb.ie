# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zombieapp', '0007_auto_20160319_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='guest',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
