from rest_framework import serializers
from models import *


class CloudSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cloud
        exclude = ('creator', 'updated_on')


class NetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        exclude = ('creator', 'created_on', 'updated_on',)


class RouterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Router
        exclude = ('creator', 'created_on', 'updated_on',)


class TenantSerializer(serializers.ModelSerializer):
    networks = NetworkSerializer(many=True, read_only=True)
    routers = RouterSerializer(many=True, read_only=True)

    class Meta:
        model = Tenant
        exclude = ('creator', 'created_on', 'updated_on',)


# class TrafficTenantSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = TrafficTenants


class TrafficListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Traffic
        exclude = ('creator', 'updated_on',)


class TrafficRetrieveSerializer(serializers.ModelSerializer):
    tenants = TenantSerializer(many=True)

    class Meta:
        model = Traffic
        fields = ('id', 'cloud', 'name', 'allowed_delta_percentage', 'test_result_path',
                  'number_of_workers', 'remote_user', 'remote_pass', 'test_method',
                  'iperf_duration', 'tenant_type', 'tenants', 'external_host', 'ssh_gateway',)


class TrafficSerializer(serializers.ModelSerializer):

    class Meta:
        model = Traffic
        fields = ('id', 'cloud', 'name', 'allowed_delta_percentage', 'test_result_path',
                  'number_of_workers', 'remote_user', 'remote_pass', 'test_method',
                  'iperf_duration', 'tenant_type', 'tenants', 'external_host', 'ssh_gateway',)
