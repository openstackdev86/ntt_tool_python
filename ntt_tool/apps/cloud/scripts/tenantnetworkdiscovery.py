from django.db import transaction
from keystoneclientutils import KeystoneClientUtils
from neutronclientutils import NeutronClientUtils
from ntt_tool.apps.cloud.models import Tenant, Network, Router
from ntt_tool.apps.cloud.serializers import TenantSerializer


class TenantDiscovery(KeystoneClientUtils):

    def get_tenants(self):
        keystone = self.get_client_instance()
        return keystone.tenants.list()


class NetworkRouterDiscovery(NeutronClientUtils):

    def get_networks_and_routers(self, user, cloud_id, tenants):
        neutron = self.get_client_instance()

        discovery_result = []

        with transaction.atomic():
            Tenant.objects.filter(cloud_id=cloud_id).delete()

            for tenant in tenants:
                tenant_obj = Tenant()
                tenant_obj.cloud_id = cloud_id
                tenant_obj.tenant_id = tenant.id
                tenant_obj.tenant_name = tenant.name
                tenant_obj.description = tenant.description
                tenant_obj.enabled = tenant.enabled
                tenant_obj.creator = user
                tenant_obj.save()

                # ToDo: Need to update status, vlan, network_cidr
                networks_list = []
                networks = neutron.list_networks(tenant_id=tenant.id)
                for network in networks.get("networks", []):
                    network_obj = Network()
                    network_obj.tenant = tenant_obj
                    network_obj.network_name = network.get("name")
                    # ToDo: We are assuming that each network is having only one subnet
                    # ToDo: Need to handle the scenario if we add more than one subnet for a network
                    if network.get("subnets"):
                        subnet_list = neutron.list_subnets(id=network.get("subnets"))
                        network_obj.network_cidr = subnet_list.get("subnets")[0].get("cidr")
                    network_obj.status = network.get("status")
                    network_obj.creator = user
                    networks_list.append(network_obj)
                Network.objects.bulk_create(networks_list)

                # ToDo: Need to update status
                routers_list = []
                routers = neutron.list_routers(tenant_id=tenant.id)
                for router in routers.get("routers", []):
                    router_obj = Router()
                    router_obj.tenant = tenant_obj
                    router_obj.router_id = router.get("id")
                    router_obj.router_name = router.get("name")
                    router_obj.status = router.get("status")
                    router_obj.creator = user
                    routers_list.append(router_obj)
                Router.objects.bulk_create(routers_list)

                serializer = TenantSerializer(tenant_obj)
                discovery_result.append(serializer.data)
        return discovery_result
