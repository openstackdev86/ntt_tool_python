from django.db import transaction
from django.utils import timezone
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
            discovery_datetime = timezone.now()

            Tenant.objects.filter(cloud_id=cloud_id).update(is_dirty=False)
            for tenant in tenants:
                tenant_obj = None
                try:
                    tenant_obj = Tenant.objects.filter(tenant_name=tenant.name).get()
                except Tenant.DoesNotExist:
                    tenant_obj = Tenant()
                tenant_obj.cloud_id = cloud_id
                tenant_obj.tenant_id = tenant.id
                tenant_obj.tenant_name = tenant.name
                tenant_obj.description = tenant.description
                tenant_obj.enabled = tenant.enabled
                tenant_obj.creator = user
                tenant_obj.is_dirty = True
                tenant_obj.updated_on = discovery_datetime
                tenant_obj.save()

                # Setting all records belongs to tenant as not dirty/updated
                Network.objects.filter(tenant__tenant_id=tenant.id)\
                    .update(is_dirty=False)
                networks = neutron.list_networks(tenant_id=tenant.id)
                for network in networks.get("networks", []):
                    network_obj = None
                    try:
                        filters = {
                            "tenant__tenant_id": tenant.id,
                            "network_name": network.get("name")
                        }
                        network_obj = Network.objects.filter(**filters).get()
                    except Network.DoesNotExist:
                        network_obj = Network()
                    network_obj.tenant = tenant_obj
                    network_obj.network_id = network.get("id")
                    network_obj.network_name = network.get("name")
                    network_obj.shared = network.get("shared")
                    # ToDo: We are assuming that each network is having only one subnet
                    # ToDo: Need to handle the scenario if we add more than one subnet for a network
                    if network.get("subnets"):
                        subnet_list = neutron.list_subnets(id=network.get("subnets"))
                        network_obj.network_cidr = subnet_list.get("subnets")[0].get("cidr")
                    network_obj.status = network.get("status")
                    network_obj.is_dirty = True
                    network_obj.creator = user
                    network_obj.updated_on = discovery_datetime
                    network_obj.save()
                # Deleting networks which are not got changed after discovery
                Network.objects.filter(tenant__tenant_id=tenant_obj.id)\
                    .filter(is_dirty=False).delete()

                # Setting all records belongs to tenant as not dirty/updated
                Router.objects.filter(tenant__tenant_id=tenant.id)\
                    .update(is_dirty=False)
                routers = neutron.list_routers(tenant_id=tenant.id)
                for router in routers.get("routers", []):
                    router_obj = None
                    try:
                        filters = {
                            "tenant__tenant_id": tenant.id,
                            "router_name": router.get("name")
                        }
                        router_obj = Router.objects.filter(**filters).get()
                    except Router.DoesNotExist:
                        router_obj = Router()
                        router_obj.created_on = discovery_datetime
                    router_obj.tenant = tenant_obj
                    router_obj.router_id = router.get("id")
                    router_obj.router_name = router.get("name")
                    router_obj.status = router.get("status")
                    router_obj.is_dirty = True
                    router_obj.creator = user
                    router_obj.updated_on = discovery_datetime
                    router_obj.save()
                # Deleting routers which are got changed after discovery
                Router.objects.filter(tenant__tenant_id=tenant_obj.id)\
                    .filter(is_dirty=False).delete()

                # Deleting tenants which are got changed after discovery
                Tenant.objects.filter(cloud_id=cloud_id)\
                    .filter(is_dirty=False).delete()

                serializer = TenantSerializer(tenant_obj)
                discovery_result.append(serializer.data)
        return discovery_result
