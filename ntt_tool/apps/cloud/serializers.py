from rest_framework import serializers
from models import *


class CloudSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cloud
        exclude = ('updated_on',)


class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenants


class CloudTrafficRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = CloudTraffic
        exclude = ('created_on', 'updated_on')
        depth = 1


class CloudTrafficSerializer(serializers.ModelSerializer):

    class Meta:
        model = CloudTraffic




