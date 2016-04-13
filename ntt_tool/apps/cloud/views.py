import json
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from models import *
from serializers import *
from openstackscripts.keystoneclientutils import KeystoneClientUtils
from openstackscripts.novaclientutils import NovaClientUtils
from openstackscripts.tenantnetworkdiscovery import *
from openstackscripts.credentials import *
from openstackscripts.endpointdiscovery import DiscoverEndpoints


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

        keystone_utils = KeystoneClientUtils(**get_credentials(cloud))
        tenants = keystone_utils.get_tenants()

        network_subnets_discovery = NetworkSubnetDiscovery(**get_credentials(cloud))
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
        with transaction.atomic():
            tenant = Tenant.objects.filter(tenant_id=tenant_id).get()

            traffic = Traffic.objects.get(pk=pk)
            traffic.tenants.clear()
            traffic.selected_networks.clear()
            traffic.tenants.add(tenant)
            traffic.save()
            TrafficNetworksMap.objects.filter(traffic=traffic).delete()

            serializer = TenantSerializer(tenant)
            return Response(serializer.data)

    @detail_route(methods=["get"], url_path="select/network")
    def select_network(self, request, pk=None):
        with transaction.atomic():
            traffic = Traffic.objects.get(pk=pk)
            if json.loads(request.GET.get("is_selected")):
                network = Network.objects.get(pk=request.GET.get("network_id"))
                traffic_network_map, created = TrafficNetworksMap.objects.get_or_create(traffic=traffic, network=network)
                traffic_network_map.save()

                # Subnet id of the first subnet of a network
                subnet_obj = network.subnets.all()[0]
                neutron_utils = NeutronClientUtils(**get_credentials(traffic.cloud))
                subnet = neutron_utils.show_subnet(subnet_id=subnet_obj.subnet_id)
                subnet_obj.allocation_pool_start = subnet.get("allocation_pools")[0].get("start")
                subnet_obj.allocation_pool_end = subnet.get("allocation_pools")[0].get("end")
                subnet_obj.save()

                serializer = SubnetSerializer(subnet_obj)
                return Response(serializer.data)

            TrafficNetworksMap.objects.filter(traffic=traffic)\
                .filter(network_id=request.GET.get("network_id")).delete()
        return Response(status.HTTP_200_OK)

    @detail_route(methods=["get"], url_path="endpoints")
    def endpoints(self, request, pk=None):
        endpoints = Endpoint.objects.filter(traffic_id=pk)
        serializer = EndpointSerializer(endpoints, many=True)
        return Response(serializer.data)

    @detail_route(methods=["post"], url_path="endpoints/discover")
    def discover_endpoints(self, request, pk=None):
        response = []
        for selected_range in json.loads(request.data.get("json", '[]')):
            network_id = selected_range.get("network_id")
            filters = {
                "traffic_id": pk,
                "network_id": network_id
            }
            obj = TrafficNetworksMap.objects.filter(**filters).get()
            obj.ip_range_start = selected_range.get("ip_range_start")
            obj.ip_range_end = selected_range.get("ip_range_end")
            obj.save()

            endpoint_discovery = DiscoverEndpoints(pk, network_id)
            endpoints = endpoint_discovery.get_endpoints(obj.ip_range_start, obj.ip_range_end)
            response.extend(endpoints)
        serializer = EndpointSerializer(response, many=True)
        return Response(serializer.data)

    @detail_route(methods=["post"], url_path="endpoints/launch")
    def launch_endpoints(self, request, pk=None):
        response = []
        traffic = Traffic.objects.get(pk=pk)
        nova_client_utils = NovaClientUtils(**get_nova_credentials(traffic.cloud))

        for selected_item in json.loads(request.data.get("json", '[]')):
            filters = {
                "traffic_id": pk,
                "network_id": selected_item.get("network_id")
            }
            obj, created = TrafficNetworksMap.objects.get_or_create(**filters)
            obj.endpoint_count = selected_item.get("endpoint_count")
            obj.save()

            network = Network.objects.get(pk=selected_item.get("network_id"))
            endpoint_name = "-".join([network.tenant.tenant_name, network.network_name])
            endpoints = nova_client_utils.launch_endpoint(network.tenant.tenant_id,
                                                          network.network_id,
                                                          endpoint_name,
                                                          selected_item.get("endpoint_count"))
            response.append(endpoints)
        return Response(True)
