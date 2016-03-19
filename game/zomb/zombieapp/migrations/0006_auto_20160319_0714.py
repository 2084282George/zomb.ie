# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('zombieapp', '0005_player_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='pcr',
        ),
        migrations.RemoveField(
            model_name='player',
            name='pgs',
        ),
        migrations.RemoveField(
            model_name='player',
            name='pps',
        ),
        migrations.RemoveField(
            model_name='player',
            name='ps',
        ),
        migrations.RemoveField(
            model_name='player',
            name='psf',
        ),
        migrations.RemoveField(
            model_name='player',
            name='ptl',
        ),
        migrations.RemoveField(
            model_name='player',
            name='pus',
        ),
        migrations.AlterField(
            model_name='player',
            name='game',
            field=picklefield.fields.PickledObjectField(editable=False),
        ),
        migrations.AlterField(
            model_name='player',
            name='picture',
            field=models.ImageField(upload_to=b'profile_pictures', blank=True),
        ),
    ]
