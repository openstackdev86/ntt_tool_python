import ConfigParser
from models import Cloud


class TenantDiscoveryController(object):

    def generate_config(self, cloud_id):
        """
        Function to generate config.ini file which is used as a input to
        tenant discovery script
        :return: True if success else False
        """
        config = ConfigParser.ConfigParser()
        try:
            cloud = Cloud.objects.get(pk=cloud_id)
            config.set(ConfigParser.DEFAULTSECT, "keystone_auth_url", cloud.keystone_auth_url)
            config.set(ConfigParser.DEFAULTSECT, "keystone_user", cloud.keystone_user)
            config.set(ConfigParser.DEFAULTSECT, "keystone_password", cloud.keystone_password)
            config.set(ConfigParser.DEFAULTSECT, "keystone_tenant_name", cloud.keystone_tenant_name)
        except Cloud.DoesNotExist:
            return False

        with open('config.ini', 'wb') as f:
            config.write(f)

        return True

    def discover_tenants(self, cloud_id):
        self.generate_config(cloud_id)
        return []






