# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-15 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20170415_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cover',
            field=models.ImageField(null=True, upload_to='covers', verbose_name='miniatura'),
        ),
    ]