# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-29 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CmdbServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name=b'\xe8\xb5\x84\xe4\xba\xa7\xe5\xba\x8f\xe5\x88\x97\xe5\x8f\xb7')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name=b'\xe7\xae\xa1\xe7\x90\x86IP\xe5\x9c\xb0\xe5\x9d\x80')),
                ('hostname', models.CharField(blank=True, max_length=64, null=True, verbose_name=b'\xe4\xb8\xbb\xe6\x9c\xba\xe5\x90\x8d')),
                ('cpu_all_core', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'\xe7\x89\xa9\xe7\x90\x86CPU\xe4\xb8\xaa\xe6\x95\xb0*\xe6\xaf\x8fCPU\xe6\xa0\xb8\xe6\x95\xb0\xef\xbc\x88\xe6\x97\xa0\xe8\xb6\x85\xe7\xba\xbf\xe7\xa8\x8b\xef\xbc\x89')),
                ('mem_size', models.IntegerField(blank=True, null=True, verbose_name=b'\xe5\x86\x85\xe5\xad\x98\xe5\xa4\xa7\xe5\xb0\x8f(GB)')),
                ('disk_size', models.FloatField(blank=True, null=True, verbose_name=b'\xe6\x9c\xac\xe5\x9c\xb0\xe6\x89\x80\xe6\x9c\x89\xe7\xa3\x81\xe7\x9b\x98\xe6\x80\xbb\xe5\x92\x8c(GB)')),
                ('asset_type', models.CharField(choices=[(b'server', b'\xe7\x89\xa9\xe7\x90\x86\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8'), (b'virtual', b'\xe8\x99\x9a\xe6\x8b\x9f\xe6\x9c\xba'), (b'other', b'\xe5\x85\xb6\xe4\xbb\x96')], default=b'server', max_length=64, verbose_name=b'\xe8\xb5\x84\xe4\xba\xa7\xe7\xb1\xbb\xe5\x9e\x8b')),
                ('os_release', models.CharField(blank=True, max_length=64, null=True, verbose_name=b'\xe6\x93\x8d\xe4\xbd\x9c\xe7\xb3\xbb\xe7\xbb\x9f\xe7\x89\x88\xe6\x9c\xac')),
                ('created_by', models.CharField(choices=[(b'auto', b'\xe8\x87\xaa\xe5\x8a\xa8\xe6\xb7\xbb\xe5\x8a\xa0'), (b'manual', b'\xe6\x89\x8b\xe5\xb7\xa5\xe5\xbd\x95\xe5\x85\xa5')], default=b'auto', max_length=32, verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x96\xb9\xe5\xbc\x8f')),
                ('update_time', models.DateField(auto_now=True)),
            ],
        ),
    ]