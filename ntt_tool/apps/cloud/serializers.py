from rest_framework import serializers
from models import *


class CloudSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cloud


class CloudTrafficListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CloudTraffic


class CloudTrafficRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = CloudTraffic
        depth = 1
        exclude = ('created_on', 'updated_on')


class CloudTrafficSerializer(serializers.ModelSerializer):

    class Meta:
        model = CloudTraffic


class CloudTrafficTenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = CloudTrafficTenants



