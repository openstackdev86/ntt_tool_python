# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-10 07:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0002_traffic_tenants'),
    ]

    operations = [
        migrations.AddField(
            model_name='traffic',
            name='ssh_gateway',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]