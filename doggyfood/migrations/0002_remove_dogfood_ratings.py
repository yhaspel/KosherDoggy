# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 19:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doggyfood', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dogfood',
            name='ratings',
        ),
    ]
