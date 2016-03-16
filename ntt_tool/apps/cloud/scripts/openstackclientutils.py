class OpenStackClientUtils(object):

    def __init__(self, username, password, auth_url, tenant_name=None):
        self.username = username
        self.password = password
        self.auth_url = auth_url
        self.tenant_name = tenant_name

    def get_credentials(self):
        return {
            "username": self.username,
            "password": self.password,
            "auth_url": self.auth_url,
            "tenant_name": self.tenant_name
        }

    def get_client_instance(self):
        credentials = self.get_credentials()
        return self.client_class(**credentials)










