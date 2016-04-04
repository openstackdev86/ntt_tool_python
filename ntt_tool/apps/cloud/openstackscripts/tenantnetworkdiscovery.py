import logging
from django.db import transaction
from django.utils import timezone
from keystoneclientutils import KeystoneClientUtils
from neutronclientutils import NeutronClientUtils
from ntt_tool.apps.cloud.models import Tenant, Network, Subnet
from ntt_tool.apps.cloud.serializers import TenantSerializer


logger = logging.getLogger(__name__)


class NetworkSubnetDiscovery(NeutronClientUtils):

    def get_networks_and_subnets(self, user, cloud_id, tenants):
        # neutron = self.get_client_instance()

        discovery_result = []
        with transaction.atomic():
            discovery_datetime = timezone.now()

            Tenant.objects.filter(cloud_id=cloud_id)\
                .update(is_dirty=False)

            for tenant in tenants:
                tenant_obj = None
                try:
                    tenant_obj = Tenant.objects.filter(tenant_id=tenant.id).get()
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

                networks = self.list_networks(tenant_id=tenant.id)
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
                    network_obj.status = network.get("status")
                    network_obj.is_dirty = True
                    network_obj.creator = user
                    network_obj.updated_on = discovery_datetime
                    network_obj.save()

                    # Setting all records belongs to tenant as not dirty/updated
                    Subnet.objects.filter(network__network_id=network.get("id"))\
                        .update(is_dirty=False)

                    subnets = self.list_subnets(network_id=network.get("id"))
                    for subnet in subnets.get("subnets"):
                        subnet_obj = None
                        try:
                            filters = {
                                "network__network_id": network.get("id"),
                                "subnet_id": subnet.get("id")
                            }
                            subnet_obj = Subnet.objects.filter(**filters).get()
                        except Subnet.DoesNotExist:
                            subnet_obj = Subnet()
                        subnet_obj.subnet_id = subnet.get("id")
                        subnet_obj.network_id = network_obj.id
                        subnet_obj.subnet_name = subnet.get("name")
                        subnet_obj.cidr = subnet.get("cidr")
                        subnet_obj.is_dirty = True
                        subnet_obj.save()

                    # Deleting subnets which are got changed after discovery
                    Subnet.objects.filter(network__network_id=network.get("id"))\
                        .filter(is_dirty=False).delete()

                # Deleting networks which are not got changed after discovery
                Network.objects.filter(tenant__tenant_id=tenant_obj.id)\
                    .filter(is_dirty=False).delete()

                serializer = TenantSerializer(tenant_obj)
                discovery_result.append(serializer.data)

            # Deleting tenants which are got changed after discovery
            Tenant.objects.filter(cloud_id=cloud_id)\
                .filter(is_dirty=False).delete()
        return discovery_result
