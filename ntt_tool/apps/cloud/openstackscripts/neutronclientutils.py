from neutronclient.v2_0 import client as neutron_client
from openstackclientutils import OpenStackClientUtils


class NeutronClientUtils(OpenStackClientUtils):
    client_class = neutron_client.Client
