from keystoneclient.v2_0 import client as keystone_client
from openstackclientutils import OpenStackClientUtils


class KeystoneClientUtils(OpenStackClientUtils):
    client_class = keystone_client.Client

    def __init__(self, **credentials):
        super(KeystoneClientUtils, self).__init__(**credentials)
        self.keystone = self.get_client_instance()

    def get_token(self):
        return self.keystone.auth_ref.get("token", {}).get("id")