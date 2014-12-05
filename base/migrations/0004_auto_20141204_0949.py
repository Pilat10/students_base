# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20141203_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='department',
            field=models.ForeignKey(to='base.Department'),
            preserve_default=True,
        ),
    ]
