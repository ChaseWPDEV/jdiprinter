# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_auto_20161218_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageLogo',
            fields=[
                ('zero', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='logos')),
            ],
        ),
    ]
