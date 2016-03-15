from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Cloud(models.Model):
    name = models.CharField(max_length=256)
    keystone_auth_url = models.CharField(max_length=2083)
    keystone_user = models.CharField(max_length=100)
    keystone_password = models.CharField(max_length=250)
    keystone_tenant_name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cloud_details"


class Tenant(models.Model):
    cloud = models.ForeignKey(Cloud, blank=True, null=True, related_name="tenants")
    tenant_id = models.CharField(max_length=100)
    tenant_name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    enabled = models.BooleanField()
    creator = models.ForeignKey(User, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cloud_tenants"


class Network(models.Model):
    tenant = models.ForeignKey(Tenant, related_name="networks")
    network_name = models.CharField(max_length=255)
    network_cidr = models.CharField(max_length=255)
    subnet = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=25)
    creator = models.ForeignKey(User, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cloud_tenant_networks"


class Router(models.Model):
    tenant = models.ForeignKey(Tenant, related_name="routers")
    router_id = models.CharField(max_length=255)
    router_name = models.CharField(max_length=255)
    status = models.CharField(max_length=25)
    creator = models.ForeignKey(User, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cloud_tenant_routers"


class Traffic(models.Model):
    TYPE_CHOICES = (
        ('all', 'All'),
        ('intra-tenant', 'Intra Tenant'),
        ('inter-tenant', 'Inter Tenant'),
        ('south-north', 'South to North'),
        ('north-south', 'North to South'),
    )

    cloud = models.ForeignKey(Cloud, blank=True, null=True, related_name="cloud_traffic")
    name = models.CharField(max_length=256)
    allowed_delta_percentage = models.FloatField()
    test_result_path = models.CharField(max_length=250)
    number_of_workers = models.IntegerField()
    remote_user = models.CharField(max_length=100)
    remote_pass = models.CharField(max_length=100)
    test_method = models.CharField(max_length=100)
    iperf_duration = models.IntegerField()
    tenant_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='all')
    tenants = models.ManyToManyField(Tenant, blank=True, null=True)
    external_host = models.CharField(max_length=100, blank=True, null=True)
    ssh_gateway = models.CharField(max_length=100, blank=True, null=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cloud_traffic"


# class TrafficTenant(models.Model):
#     traffic = models.ForeignKey(Traffic)
#     tenant = models.ForeignKey(Tenant)