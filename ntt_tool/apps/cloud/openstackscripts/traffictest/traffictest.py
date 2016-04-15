import time
from ntt_tool.apps.cloud.models import Traffic
from utils import *
from ntt_tool.apps.cloud.openstackscripts.traffictest.libs import traf_tester


class TrafficTest(object):

    def __init__(self, traffic_id):
        self.traffic = Traffic.objects.get(pk=traffic_id)

    def run_test(self):
        endpoints_list = self.generate_endpoints_contract_list()
        setup_config = self.generate_setup_config()
        traf_tester.start_task(setup_config, endpoints_list, 'start', "devtest")
        time.sleep(60)
        traf_tester.start_task(setup_config, endpoints_list, 'stop', "devtest")

    def stop_test(self):
        pass

    def generate_endpoints_contract_list(self):
        endpoint_configs = []
        if self.traffic.test_type == 'intra-tenant':
            config = {
                'contract': [],
                'test_type': self.traffic.test_type,
                'src_tenant': [x.tenant_name for x in self.traffic.tenants.all()],
                'dest_eps': ['3.3.3.3'],
                'src_eps': ['2.2.2.9', '2.2.2.10']
            }
            for test_method in self.traffic.test_method.split(','):
                config.get('contract').append(test_method_contracts(test_method))
            config['dest_tenant'] = config['src_tenant']
            endpoint_configs.append(config)
        return endpoint_configs

    def generate_setup_config(self):
        setup_config = {}
        cloud = self.traffic.cloud
        setup_config['default'] = {
            'keystone_auth_url': cloud.keystone_auth_url,
            'keystone_user': cloud.keystone_user,
            'keystone_password': cloud.keystone_password,
            'keystone_tenant_name': cloud.keystone_tenant_name
        }
        setup_config['traffic'] = {
            'allowed_delta_percentage': self.traffic.allowed_delta_percentage,
            'test_results_path': self.traffic.test_result_path,
            'number_of_workers': self.traffic.number_of_workers,
            'remote_user': self.traffic.remote_user,
            'remote_pass': self.traffic.remote_pass,
            'test_method': self.traffic.test_method.split(','),
            'iperf_duration': self.traffic.iperf_duration,
            'type': self.traffic.test_type
        }
        setup_config['tenants'] = {'tenants': []}
        setup_config['tenant_ssh_gateway'] = {}
        for tenant in self.traffic.tenants.all():
            setup_config['tenants']['tenants'].append(tenant.tenant_name)
            setup_config['tenant_ssh_gateway'][tenant.tenant_name] = self.traffic.ssh_gateway
        setup_config['external_host'] = {'host': self.traffic.external_host}
        return setup_config
