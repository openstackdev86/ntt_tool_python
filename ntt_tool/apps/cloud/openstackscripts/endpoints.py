from netaddr import IPRange
from django.db import transaction
from neutronclient.v2_0 import client as neutron_client
from novaclient.v1_1 import client as nova_client
from ntt_tool.apps.cloud.models import Network, Endpoint
from credentials import *
from novaclientutils import NovaClientUtils


class DiscoverEndpoints(object):

    def __init__(self, traffic_id, network_id):
        self.traffic_id = traffic_id
        self.network = Network.objects.get(pk=network_id)
        self.neutron = neutron_client.Client(**get_credentials(self.network.tenant.cloud))
        self.nova = nova_client.Client(**get_nova_credentials(self.network.tenant.cloud))

    def get_endpoints(self, ip_range_start, ip_range_end):
        ip_range = IPRange(ip_range_start, ip_range_end)
        subnet = self.network.subnets.first()
        ports = self.neutron.list_ports(network_id=self.network.network_id).get('ports')
        endpoints = []
        with transaction.atomic():
            Endpoint.objects.filter(traffic_id=self.traffic_id).update(is_dirty=False)
            for port in ports:
                if port.get("device_owner") == "compute:nova":
                    if port['fixed_ips'][0]['subnet_id'] == subnet.subnet_id:
                        endpoint = self.nova.servers.get(port['device_id'].encode('unicode_escape'))
                        if endpoint and endpoint.status == 'ACTIVE':
                            ip_address = port['fixed_ips'][0]['ip_address'].encode('unicode_escape')
                            if ip_address in ip_range:
                                filters = {
                                    "traffic_id": self.traffic_id,
                                    "network_id": self.network.id,
                                    "endpoint_id": endpoint.id
                                }
                                endpoint_obj, created = Endpoint.objects.get_or_create(**filters)
                                endpoint_obj.endpoint_id = endpoint.id
                                endpoint_obj.name = endpoint.name
                                endpoint_obj.ip_address = ip_address
                                endpoint_obj.status = endpoint.status
                                endpoint_obj.is_dirty = True
                                endpoint_obj.save()
                                endpoints.append(endpoint_obj)
            Endpoint.objects.filter(traffic_id=self.traffic_id).filter(is_dirty=False).delete()
        return endpoints


class LaunchEndpoints(NovaClientUtils):

    def __init__(self, traffic, network_id, **credentials):
        super(LaunchEndpoints, self).__init__(**credentials)
        self.traffic = traffic
        self.network = Network.objects.get(pk=network_id)

    def launch(self, endpoint_count=1):
        endpoints = []
        endpoint_name = "-".join([self.network.tenant.tenant_name, self.network.network_name])
        launched_endpoints = self.launch_endpoint(self.network.tenant.tenant_id,
                                                 self.network.network_id,
                                                 endpoint_name,
                                                 endpoint_count)

        with transaction.atomic():
            filters = {
                "traffic_id": self.traffic.id,
                "network_id": self.network.id,
            }
            Endpoint.objects.filter(**filters).update(is_dirty=False)
            for endpoint in launched_endpoints:
                endpoint_obj, created = Endpoint.objects.get_or_create(traffic_id=self.traffic.id,
                                                                       network_id=self.network.id,
                                                                       endpoint_id=endpoint.id)
                endpoint_obj.name = endpoint.name
                endpoint_obj.ip_address = endpoint.addresses.get(self.network.network_name)[0].get("addr")
                endpoint_obj.status = endpoint.status
                endpoint_obj.is_dirty = True
                endpoint_obj.save()
                endpoints.append(endpoint_obj)
            Endpoint.objects.filter(**filters).filter(is_dirty=False).delete()
        return endpoints
