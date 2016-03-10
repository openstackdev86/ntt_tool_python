from rest_framework import serializers
from models import *


class CloudSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cloud
        exclude = ('creator', 'updated_on')


class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenants
        exclude = ('remote_pass', 'external_host', 'tenants', 'creator', 'created_on', 'updated_on',)


class TrafficListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Traffic
        exclude = ('creator', 'updated_on',)


class TrafficRetrieveSerializer(serializers.ModelSerializer):
    available_tenants = serializers.SerializerMethodField()
    selected_tenants = serializers.SerializerMethodField()

    def get_available_tenants(self, obj):
        available = [
            {"id": 1, "name": "tenant-test-101", "router_name": "tenant-test-101-router", "network_name": "tenant-test-101-net-1", "network_cidr": "1.1.1.0/24"},
            {"id": 2, "name": "tenant-test-102", "router_name": "tenant-test-102-router", "network_name": "tenant-test-101-net-1", "network_cidr": "1.1.1.0/24"},
            {"id": 3, "name": "tenant-test-103", "router_name": "tenant-test-103-router", "network_name": "tenant-test-101-net-1", "network_cidr": "2.2.2.0/24"},
        ]
        return [x for x in available if str(x.get("id")) not in obj.tenants.split(",")]

    def get_selected_tenants(self, obj):
        selected = [
            {"id": 1, "name": "tenant-test-101", "router_name": "tenant-test-101-router", "network_name": "tenant-test-101-net-1", "network_cidr": "1.1.1.0/24"},
            {"id": 2, "name": "tenant-test-102", "router_name": "tenant-test-102-router", "network_name": "tenant-test-101-net-1", "network_cidr": "1.1.1.0/24"},
            {"id": 3, "name": "tenant-test-103", "router_name": "tenant-test-103-router", "network_name": "tenant-test-101-net-1", "network_cidr": "2.2.2.0/24"},
        ]
        return [x for x in selected if str(x.get("id")) in obj.tenants.split(",")]

    class Meta:
        model = Traffic
        exclude = ('creator', 'created_on', 'updated_on',)


class TrafficSerializer(serializers.ModelSerializer):

    class Meta:
        model = Traffic
        exclude = ('creator', 'created_on', 'updated_on',)

