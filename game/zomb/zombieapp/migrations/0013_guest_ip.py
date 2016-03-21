# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('zombieapp', '0012_auto_20160320_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='ip',
            field=picklefield.fields.PickledObjectField(default=b'', editable=False),
            preserve_default=True,
        ),
    ]
