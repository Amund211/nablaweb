# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-26 13:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20171017_0110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='view_counter',
        ),
    ]
