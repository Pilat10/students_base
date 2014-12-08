# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_department', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('department', models.ForeignKey(related_name='++', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Department', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_flag', models.PositiveSmallIntegerField(choices=[(1, b'add'), (2, b'change'), (3, b'delete')])),
                ('action_time', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('object_descript', models.TextField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fio', models.CharField(max_length=255)),
                ('birthday', models.DateField()),
                ('number_student_cart', models.IntegerField()),
                ('group', models.ForeignKey(to='base.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='group',
            name='headman',
            field=models.OneToOneField(related_name='+', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Student'),
            preserve_default=True,
        ),
    ]
