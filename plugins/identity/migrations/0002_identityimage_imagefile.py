# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='identityimage',
            name='imageFile',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
