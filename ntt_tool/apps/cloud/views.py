from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import list_route
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


class CloudTenantsViewSet(viewsets.ModelViewSet):
    queryset = CloudTenants.objects.all()
    serializer_class = CloudTenantsSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        cloud_id = self.request.GET.get("cloud_id")
        queryset = self.filter_queryset(CloudTenants.objects.filter(cloud_id=cloud_id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=["get"], url_path="discover/(?P<cloud_id>[^/.]+)")
    def discover(self, request, cloud_id=None):
        return Response("I am called")


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



