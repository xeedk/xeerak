# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 01:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0003_auto_20170225_1415'),
        ('recognition', '0006_auto_20170225_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsrequest',
            name='smsIdentity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='identity.SmsIdentity'),
        ),
    ]
