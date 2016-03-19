# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('zombieapp', '0003_auto_20160318_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='pcr',
            field=picklefield.fields.PickledObjectField(default='', editable=False),
            preserve_default=False,
        ),
    ]
