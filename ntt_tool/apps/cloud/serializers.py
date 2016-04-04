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


class TrafficRetrieveSerializer(serializers.ModelSerializer):
    tenants = TenantSerializer(many=True, required=False)
    selected_network = NetworkSerializer(many=True, read_only=True)

    class Meta:
        model = Traffic
        exclude = ('creator', 'updated_on',)

    # def create(self, validated_data):
    #     # get tenants
    #     tenants_data = validated_data.pop("tenants")
    #     # create traffic instance
    #     traffic = self.Meta.model.objects.create(**validated_data)
    #     for tenant_id in tenants_data:
    #         traffic.tenants.add(tenant_id)
    #     traffic.save()
    #     return traffic
    #
    # def update(self, instance, validated_data):
    #     # get tenants
    #     instance.tenants.clear()
    #     tenants_data = validated_data.pop("tenants")
    #     for tenant in tenants_data:
    #         tenant_obj = Tenant.objects.filter(**tenant).get()
    #         instance.tenants.add(tenant_obj)
    #     instance.save()
    #     return instance



