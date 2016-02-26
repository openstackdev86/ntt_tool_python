from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Cloud(models.Model):
    name = models.CharField(max_length=256)
    keystone_auth_url = models.CharField(max_length=2083)
    keystone_user = models.CharField(max_length=100)
    keystone_password = models.CharField(max_length=250)
    keystone_tenant_name = models.CharField(max_length=100)
    # creator = models.ForeignKey(User) #ToDo: Facing some issues in serializer validation
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cloud_details"


class CloudTraffic(models.Model):
    TYPE_CHOICES = (
        ('all', 'All'),
        ('intra-tenant', 'Intra Tenant'),
        ('inter-tenant', 'Inter Tenant'),
        ('south-north', 'South to North'),
        ('north-south', 'North to South'),
    )

    name = models.CharField(max_length=256)
    cloud = models.ForeignKey(Cloud)
    allowed_delta_percentage = models.FloatField()
    test_result_path = models.CharField(max_length=250)
    number_of_workers = models.IntegerField()
    remote_user = models.CharField(max_length=100)
    remote_pass = models.CharField(max_length=100)
    test_method = models.CharField(max_length=100)
    iperf_duration = models.IntegerField()
    tenant_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='all')
    external_host = models.CharField(max_length=100, blank=True, null=True)
    # creator = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cloud_traffic"


class CloudTrafficTenants(models.Model):
    cloud_traffic = models.ForeignKey(CloudTraffic, related_name="cloud_traffic_tenants")
    tenant_name = models.CharField(max_length=256)
    ssh_gateway = models.CharField(max_length=256, blank=True, null=True)
    creator = models.ForeignKey(User, related_name="cloud_traffic_tenants_creator")
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cloud_traffic_tenants"
