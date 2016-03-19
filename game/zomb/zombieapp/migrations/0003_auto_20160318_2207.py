# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('zombieapp', '0002_auto_20160318_1840'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='gs',
            new_name='pgs',
        ),
        migrations.AddField(
            model_name='player',
            name='psf',
            field=picklefield.fields.PickledObjectField(default='', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='ptl',
            field=picklefield.fields.PickledObjectField(default='', editable=False),
            preserve_default=False,
        ),
    ]
