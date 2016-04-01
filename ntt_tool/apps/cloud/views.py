import json
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from models import *
from serializers import *
from openstackscripts.novaclientutils import NovaClientUtils
from openstackscripts.tenantnetworkdiscovery import *


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
    action_serializers = {
        'retrieve': TenantSerializer,
        'list': TenantSerializer,
        'create': TenantSerializer,
        'update': TenantSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(TrafficViewSet, self).get_serializer_class()

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

        network_subnets_discovery = NetworkSubnetDiscovery(**credentials)
        tenant_networks_routers = network_subnets_discovery.get_networks_and_subnets(
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
        'retrieve': TrafficRetrieveSerializer,
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

    def perform_create(self, serializer):
        serializer.save(
            tenants=self.request.data.getlist("tenants[]"),
            creator=self.request.user,
            cloud_id=self.request.data.get("cloud_id")
        )

    @detail_route(methods=["get"], url_path="select/tenant/(?P<tenant_id>[-\w]+)")
    def select_tenant(self, request, pk=None, tenant_id=None):
        traffic = Traffic.objects.get(pk=pk)
        if traffic.test_type == 'intra-tenant':
            traffic.tenants.clear()
            traffic.tenants.add(
                Tenant.objects.filter(tenant_id=tenant_id).get()
            )
        traffic.save()
        serializer = TrafficSerializer(traffic)
        return Response(serializer.data)

    @detail_route(methods=["get"], url_path="select/network")
    def select_network(self, request, pk=None):
        network = Network.objects\
            .filter(network_id=request.GET.get("network_id")).get()
        network.is_selected = json.loads(request.GET.get("is_selected"))
        network.save()
        return Response(True)

    @detail_route(methods=["get"], url_path="vm/launch")
    def launch_vm(self, request, pk=None):
        traffic = None
        try:
            traffic = Traffic.objects.get(pk=pk)
        except Cloud.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        credentials = {
            "username": traffic.cloud.keystone_user,
            "api_key": traffic.cloud.keystone_password,
            "auth_url": traffic.cloud.keystone_auth_url,
            "project_id": traffic.cloud.keystone_tenant_name
        }
        nova = NovaClientUtils(**credentials)

        instances = []
        for tenant in traffic.tenants.all():
            for count, network in enumerate(tenant.networks.all()):
                if not network.shared:
                    vm_name = "-".join([network.network_name, "vm", str(count)])
                    instance = nova.launch_vm(tenant.tenant_id,
                                               network.network_id,
                                               vm_name)
                    instances.append(instance)
        return Response(instances)

    @detail_route(methods=["get"], url_path="test")
    def test(self, request, pk=None):
        return Response("hey")