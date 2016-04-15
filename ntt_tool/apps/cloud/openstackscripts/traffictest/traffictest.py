import time
from ntt_tool.apps.cloud.models import Traffic, Endpoint
from utils import *
from ntt_tool.apps.cloud.openstackscripts.traffictest.libs import traf_tester


class TrafficTest(object):

    def __init__(self, traffic_id):
        self.traffic = Traffic.objects.get(pk=traffic_id)

    def run_test(self, traffic_test_duration=1):
        endpoints_list = self.generate_endpoints_contract_list()
        setup_config = self.generate_setup_config()
        traf_tester.start_task(setup_config, endpoints_list, "start", "_".join(self.traffic.name.split()))
        time.sleep(60 * traffic_test_duration)
        traf_tester.start_task(setup_config, endpoints_list, "stop", "_".join(self.traffic.name.split()))
        return True

    def stop_test(self):
        pass

    def generate_endpoints_contract_list(self):
        endpoint_contract_configs = []
        if self.traffic.test_type == 'intra-tenant':
            subnet_endpoints_map = {}
            endpoints = Endpoint.objects.filter(traffic_id=self.traffic.id).filter(is_selected=True)
            for endpoint in endpoints:
                subnet = endpoint.network.subnets.first()
                if subnet.subnet_name not in subnet_endpoints_map:
                    subnet_endpoints_map[subnet.subnet_name] = {
                        'endpoints': [],
                        'id': subnet.subnet_id,
                        'name': subnet.subnet_name
                    }
                subnet_endpoints_map[subnet.subnet_name]['endpoints'].append(endpoint.ip_address)

            net = {}
            for entry in subnet_endpoints_map.values():
                tsrc = []
                tdest = []
                tsrc.append(entry['endpoints'])
                for nextep in subnet_endpoints_map.values():
                    if entry['name'] != nextep['name']:
                        tdest.append(nextep['endpoints'])
                        subnet_data = {
                            'src_eps': [ep for eps in tsrc for ep in eps],
                            'dest_eps': [ep for eps in tdest for ep in eps]
                        }
                        net[entry['name']] = subnet_data

            for k, src_dst_eps in net.iteritems():
                config = {
                    'contract': [],
                    'test_type': self.traffic.test_type,
                    'src_tenant': [x.tenant_name for x in self.traffic.tenants.all()],
                    'dest_eps': src_dst_eps.get('dest_eps'),
                    'src_eps': src_dst_eps.get('src_eps')
                }
                for test_method in self.traffic.test_method.split(','):
                    config.get('contract').append(test_method_contracts(test_method))
                config['dest_tenant'] = config['src_tenant']
                endpoint_contract_configs.append(config)

        print "*"*200
        print endpoint_contract_configs
        print "\n\n\n\n"
        return endpoint_contract_configs

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
