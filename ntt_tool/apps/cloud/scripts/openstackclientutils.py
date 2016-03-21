class OpenStackClientUtils(object):

    def __init__(self, **credentials):
        self.credentials = credentials

    def get_credentials(self):
        return self.credentials

    def get_client_instance(self):
        credentials = self.get_credentials()
        return self.client_class(**credentials)










