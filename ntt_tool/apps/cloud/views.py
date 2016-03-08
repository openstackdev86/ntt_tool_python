from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import list_route, detail_route
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

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenants.objects.all()
    serializer_class = TenantSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        cloud_id = self.request.GET.get("cloud_id")
        queryset = self.filter_queryset(
                Tenants.objects.filter(cloud_id=cloud_id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=["get"], url_path="discover/(?P<cloud_id>[^/.]+)")
    def discover(self, request, cloud_id=None):
        response = {
            "total_tenants": 10,
            "total_routers": 10,
            "total_networks": 10,
            "total_vm": 10,
            "tenants": [
                {"id": 1,
                 "name": "tenant-test-101",
                 "router_name": "tenant-test-101-router",
                 "network_name": "tenant-test-101-net-1",
                 "network_cidr": "1.1.1.0/24"},
                {"id": 2,
                 "name": "tenant-test-102",
                 "router_name": "tenant-test-102-router",
                 "network_name": "tenant-test-101-net-1",
                 "network_cidr": "1.1.1.0/24"},
                {"id": 3,
                 "name": "tenant-test-103",
                 "router_name": "tenant-test-103-router",
                 "network_name": "tenant-test-101-net-1",
                 "network_cidr": "2.2.2.0/24"},
            ]
        }

        import time
        time.sleep(1)
        return Response(response)

    # def create(self, request, *args, **kwargs):
    #     import pdb
    #     pdb.set_trace()
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CloudTrafficViewSet(viewsets.ModelViewSet):
    queryset = CloudTraffic.objects.all()
    serializer_class = CloudTrafficSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        cloud_id = self.request.GET.get("cloud_id")
        queryset = self.filter_queryset(
                CloudTraffic.objects.filter(cloud_id=cloud_id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



