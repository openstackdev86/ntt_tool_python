from keystoneclient.v2_0 import client as keystone_client
from openstackclientutils import OpenStackClientUtils


class KeystoneClientUtils(OpenStackClientUtils):
    client_class = keystone_client.Client
