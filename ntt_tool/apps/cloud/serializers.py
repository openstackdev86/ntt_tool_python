from rest_framework import serializers
from models import *


class CloudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloud
        exclude = ('creator', 'updated_on')


class SubnetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subnet


class NetworkSerializer(serializers.ModelSerializer):
    subnets = SubnetSerializer(many=True, read_only=True)

    class Meta:
        model = Network
        exclude = ('creator', 'created_on', 'updated_on',)


class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Router
        exclude = ('creator', 'created_on', 'updated_on',)


class TenantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ('id', 'tenant_name', 'enabled', 'description')


class TenantSerializer(serializers.ModelSerializer):
    networks = NetworkSerializer(many=True, read_only=True)

    class Meta:
        model = Tenant
        exclude = ('creator', 'created_on', 'updated_on',)


class TrafficListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traffic
        exclude = ('creator', 'updated_on',)


class TrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traffic
        exclude = ('creator', 'updated_on',)


class TrafficNetworksMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficNetworksMap
        fields = ("network", "ip_range_start", "ip_range_end", "endpoint_count")


class TrafficRetrieveSerializer(serializers.ModelSerializer):
    tenants = TenantSerializer(many=True, required=False)
    selected_networks = serializers.SerializerMethodField()

    class Meta:
        model = Traffic
        exclude = ('creator', 'updated_on',)

    def get_selected_networks(self, traffic):
        objs = traffic.selected_networks.through.objects.filter(traffic=traffic)
        serializer = TrafficNetworksMapSerializer(objs, many=True)
        return serializer.data


class EndpointSerializer(serializers.ModelSerializer):
    network_id = serializers.IntegerField(source='network.id', read_only=True)
    network_name = serializers.CharField(source="network.network_name", read_only=True)

    class Meta:
        model = Endpoint
        fields = ('id', 'network_id', 'network_name', 'endpoint_id', 'name', 'status', 'ip_address', 'is_selected')