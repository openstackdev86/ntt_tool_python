nttApp.controller('TenantListCtrl', function($scope, tenantService){
    $scope.tenants = [
            {"id": 1, "name": "tenant-test-101", "router_name": "tenant-test-101-router", "network_name": "tenant-test-101-net-1", "network_cidr": "1.1.1.0/24"},
            {"id": 2, "name": "tenant-test-102", "router_name": "tenant-test-102-router", "network_name": "tenant-test-101-net-1", "network_cidr": "1.1.1.0/24"},
            {"id": 3, "name": "tenant-test-103", "router_name": "tenant-test-103-router", "network_name": "tenant-test-101-net-1", "network_cidr": "2.2.2.0/24"},
    ]

});

nttApp.controller('TenantDiscoveryCtrl', function($scope, $routeParams, tenantService){
    $scope.cloudId = $routeParams.cloudId;
    $scope.discoveryResult = {};

    $scope.showLoading = true;
    $scope.discover = function(){
        tenantService.discover($scope.cloudId).then(function(data){
            $scope.showLoading = false;
            $scope.discoveryResult = {
                "total_tenants": 10,
                "total_routers": 10,
                "total_networks": 10,
                "total_vm": 10,
                "tenants": [
                    {"id": 1, "name": "tenant-test-101", "router_name": "tenant-test-101-router", "network_name": "tenant-test-101-net-1", "network_cidr": "1.1.1.0/24"},
                    {"id": 2, "name": "tenant-test-102", "router_name": "tenant-test-102-router", "network_name": "tenant-test-101-net-1", "network_cidr": "1.1.1.0/24"},
                    {"id": 3, "name": "tenant-test-103", "router_name": "tenant-test-103-router", "network_name": "tenant-test-101-net-1", "network_cidr": "2.2.2.0/24"},
                ]
            };
        });
    };
    $scope.discover();

    $scope.selectedResult = {
        "cloud_id": $scope.cloudId,
        "tenants": [],
    };
    $scope.saveTenants = function () {
        tenantService.save($scope.selectedResult).then(function(data){
           console.log("Hey")
        });
    };
});