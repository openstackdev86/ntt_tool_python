from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


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
    description = models.CharField(max_length=256, blank=True, null=True)
    enabled = models.BooleanField(default=False)
    is_dirty = models.BooleanField(default=False)
    creator = models.ForeignKey(User, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cloud_tenants"


class Network(models.Model):
    tenant = models.ForeignKey(Tenant, related_name="networks")
    network_id = models.CharField(max_length=255)
    network_name = models.CharField(max_length=255)
    shared = models.BooleanField(default=False)
    status = models.CharField(max_length=25)
    is_dirty = models.BooleanField(default=False)
    creator = models.ForeignKey(User, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cloud_tenant_networks"


class Subnet(models.Model):
    network = models.ForeignKey(Network, related_name="subnets")
    subnet_id = models.CharField(max_length=255)
    subnet_name = models.CharField(max_length=255)
    cidr = models.CharField(max_length=255)
    is_dirty = models.BooleanField(default=False)

    class Meta:
        db_table = "cloud_tenant_network_subnets"


class Router(models.Model):
    tenant = models.ForeignKey(Tenant, related_name="routers")
    router_id = models.CharField(max_length=255)
    router_name = models.CharField(max_length=255)
    status = models.CharField(max_length=25)
    is_dirty = models.BooleanField(default=False)
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

    TEST_ENVIRONMENT_CHOICES = (
        ('dev', 'Development/Test'),
        ('prod', 'Production'),
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
    tenants = models.ManyToManyField(Tenant)
    external_host = models.CharField(max_length=100, blank=True, null=True)
    ssh_gateway = models.CharField(max_length=100, blank=True, null=True)
    test_environment = models.CharField(max_length=20, choices=TEST_ENVIRONMENT_CHOICES, default='dev')
    creator = models.ForeignKey(User, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cloud_traffic"

