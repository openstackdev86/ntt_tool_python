from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from models import *
from serializers import *
from scripts.tenantnetworkdiscovery import TenantDiscovery, NetworkRouterDiscovery


class CloudViewSet(viewsets.ModelViewSet):
    queryset = Cloud.objects.all()
    serializer_class = CloudSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        cloud_id = self.request.GET.get("cloud_id")
        queryset = self.filter_queryset(
                Tenant.objects.filter(cloud_id=cloud_id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=["get"], url_path="discover/(?P<cloud_id>[^/.]+)")
    def discover(self, request, cloud_id=None):
        cloud = None
        try:
            cloud = Cloud.objects.get(pk=cloud_id, creator=request.user)
        except Cloud.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        credentials = {
            "username": cloud.keystone_user,
            "password": cloud.keystone_password,
            "auth_url": cloud.keystone_auth_url,
            "tenant_name": cloud.keystone_tenant_name
        }

        tenant_discovery = TenantDiscovery(**credentials)
        tenants = tenant_discovery.get_tenants()

        network_router_discovery = NetworkRouterDiscovery(**credentials)
        tenant_networks_routers = network_router_discovery.get_networks_and_routers(
                request.user,
                cloud_id,
                tenants
        )
        return Response(tenant_networks_routers)


class TrafficViewSet(viewsets.ModelViewSet):
    queryset = Traffic.objects.all()
    serializer_class = TrafficSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    action_serializers = {
        'retrieve': TrafficSerializer,
        'list': TrafficListSerializer,
        'create': TrafficSerializer,
        'update': TrafficSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(TrafficViewSet, self).get_serializer_class()

    def list(self, request, *args, **kwargs):
        cloud_id = self.request.GET.get("cloud_id")
        queryset = self.filter_queryset(
                Traffic.objects.filter(cloud_id=cloud_id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def parse_tenants(self):
        return ",".join([str(x) for x in self.request.data.get("tenants", [])])

    def create(self, request, *args, **kwargs):
        import pdb
        pdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        import pdb
        pdb.set_trace()

        serializer.save(
            # tenants=self.parse_tenants(),
            creator=self.request.user,
            cloud_id=self.request.data.get("cloud_id")
        )

    def perform_update(self, serializer):
        serializer.save(
            tenants=self.parse_tenants(),
        )

    @detail_route(methods=["get"], url_path="test")
    def test(self, request, pk=None):
        return Response("hey")