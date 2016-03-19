# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('zombieapp', '0004_player_pcr'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='game',
            field=picklefield.fields.PickledObjectField(default=b'', editable=False),
            preserve_default=True,
        ),
    ]
