from neutronclient.v2_0 import client as neutron_client
from openstackclientutils import OpenStackClientUtils


class NeutronClientUtils(OpenStackClientUtils):
    client_class = neutron_client.Client

    def __init__(self, **credentials):
        super(NeutronClientUtils, self).__init__(**credentials)
        self.neutron = self.get_client_instance()

    def list_networks(self, **kwargs):
        return self.neutron.list_networks(**kwargs)

    def list_subnets(self, **kwargs):
        return self.neutron.list_subnets(**kwargs)

    def show_subnet(self, subnet_id):
        return self.neutron.show_subnet(subnet_id).get("subnet")
