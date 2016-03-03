# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-03 07:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cloud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('keystone_auth_url', models.CharField(max_length=2083)),
                ('keystone_user', models.CharField(max_length=100)),
                ('keystone_password', models.CharField(max_length=250)),
                ('keystone_tenant_name', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cloud_details',
            },
        ),
        migrations.CreateModel(
            name='CloudTraffic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('allowed_delta_percentage', models.FloatField()),
                ('test_result_path', models.CharField(max_length=250)),
                ('number_of_workers', models.IntegerField()),
                ('remote_user', models.CharField(max_length=100)),
                ('remote_pass', models.CharField(max_length=100)),
                ('test_method', models.CharField(max_length=100)),
                ('iperf_duration', models.IntegerField()),
                ('tenant_type', models.CharField(choices=[('all', 'All'), ('intra-tenant', 'Intra Tenant'), ('inter-tenant', 'Inter Tenant'), ('south-north', 'South to North'), ('north-south', 'North to South')], default='all', max_length=20)),
                ('external_host', models.CharField(blank=True, max_length=100, null=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('cloud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloud.Cloud')),
            ],
            options={
                'db_table': 'cloud_traffic',
            },
        ),
        migrations.CreateModel(
            name='CloudTrafficTenants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_name', models.CharField(max_length=256)),
                ('ssh_gateway', models.CharField(blank=True, max_length=256, null=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('cloud_traffic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cloud_traffic_tenants', to='cloud.CloudTraffic')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cloud_traffic_tenants_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cloud_traffic_tenants',
            },
        ),
    ]
