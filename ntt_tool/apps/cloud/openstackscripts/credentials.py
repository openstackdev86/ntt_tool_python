from ntt_tool.apps.cloud.models import Cloud


def get_cloud_instance(cloud):
    if not isinstance(cloud, Cloud):
        return Cloud.objects.get(pk=cloud)
    return cloud


def get_credentials(cloud):
    try:
        cloud = get_cloud_instance(cloud)
        credentials = {
            "username": cloud.keystone_user,
            "password": cloud.keystone_password,
            "auth_url": cloud.keystone_auth_url,
            "tenant_name": cloud.keystone_tenant_name
        }
        return credentials
    except Exception, e:
        return {}


def get_nova_credentials(cloud):
    try:
        cloud = get_cloud_instance(cloud)
        credentials = {
            "username": cloud.keystone_user,
            "password": cloud.keystone_password,
            "auth_url": cloud.keystone_auth_url,
            "project_id": cloud.keystone_tenant_name
        }
        return credentials
    except Exception, e:
        return {}