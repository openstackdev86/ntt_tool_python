from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from models import *
from serializers import *


class CloudViewSet(viewsets.ModelViewSet):
    queryset = Cloud.objects.all()
    serializer_class = CloudSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CloudTrafficViewSet(viewsets.ModelViewSet):
    queryset = CloudTraffic.objects.all()
    serializer_class = CloudTrafficSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        cloud_id = self.request.GET.get("cloud_id")
        queryset = self.filter_queryset(CloudTraffic.objects.filter(cloud_id=cloud_id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CloudTrafficTenantsViewSet(viewsets.ModelViewSet):
    queryset = CloudTrafficTenants.objects.all()
    serializer_class = CloudTrafficTenantSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        traffic_id = self.request.GET.get("traffic_id")
        queryset = self.filter_queryset(CloudTrafficTenants.objects.filter(cloud_traffic_id=traffic_id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        tenant = CloudTrafficTenants()
        tenant.cloud_traffic_id = request.data.get("cloud_traffic_id")
        tenant.tenant_name = request.data.get("tenant_name")
        tenant.ssh_gateway = request.data.get("ssh_gateway")
        tenant.creator = request.user
        tenant.save()

        serializer = CloudTrafficTenantSerializer(tenant)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

