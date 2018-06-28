# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-29 09:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devops', '0002_cmdbserver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmdbserver',
            name='disk_size',
            field=models.FloatField(blank=True, db_column=b'\xe7\xa3\x81\xe7\x9b\x98\xe6\x80\xbb\xe5\x92\x8c(GB)', null=True, verbose_name=b'\xe6\x9c\xac\xe5\x9c\xb0\xe6\x89\x80\xe6\x9c\x89\xe7\xa3\x81\xe7\x9b\x98\xe6\x80\xbb\xe5\x92\x8c(GB)'),
        ),
        migrations.AlterField(
            model_name='cmdbserver',
            name='mem_size',
            field=models.IntegerField(blank=True, db_column=b'\xe5\x86\x85\xe5\xad\x98(GB)', null=True, verbose_name=b'\xe5\x86\x85\xe5\xad\x98\xe5\xa4\xa7\xe5\xb0\x8f(GB)'),
        ),
    ]
