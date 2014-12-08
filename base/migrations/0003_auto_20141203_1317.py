# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20141203_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='department',
            field=models.ForeignKey(related_name='++', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Department', null=True),
            preserve_default=True,
        ),
    ]
