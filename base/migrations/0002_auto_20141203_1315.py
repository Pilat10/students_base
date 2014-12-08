# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='department',
            field=models.ForeignKey(related_name='++', on_delete=django.db.models.deletion.SET_NULL, default=0, blank=True, to='base.Department', null=True),
            preserve_default=True,
        ),
    ]
