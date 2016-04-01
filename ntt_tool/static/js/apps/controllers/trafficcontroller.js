nttApp.controller('TrafficListCtrl', function($scope, $routeParams, trafficService){
    $scope.trafficList = [];
    trafficService.list($routeParams.id).then(function(response){
        $scope.trafficList = response;
    });

    $scope.delete = function($index){
        if (confirm("Are you sure want to delete?")){
            trafficService.delete($scope.trafficList[$index].id).then(function(response){
                $scope.trafficList.splice($index, 1);
            });
        }
    };
});


nttApp.controller('TrafficCtrl', function($scope, $routeParams, $location, trafficService, tenantService){
    $scope.cloudId = $routeParams.cloudId;
    $scope.id = $routeParams.id;
    $scope.event = $scope.id == undefined ? "add" : "edit";
    $scope.traffic = {
        "cloud_id": $scope.cloudId,
        "test_type": "intra-tenant",
        "test_method": "icmp",
        "test_environment": "dev",
    };

    if ($scope.event == "edit"){
        trafficService.get($scope.id).then(function(response){
            $scope.traffic = response;
        });
    }

    $scope.save = function(){
        if($scope.event == "add") {
            trafficService.create($scope.traffic).then(function (response) {
                $location.path("cloud/traffic/view/" + $scope.cloudId + "/" + response.id + "/");
            });
        }
        else {
            trafficService.update($scope.traffic.id, $scope.traffic).then(function(response){
                $location.path("cloud/traffic/view/" + $scope.cloudId + "/" + $scope.traffic.id + "/");
            });
        }
    };
});


nttApp.controller('TrafficViewCtrl', function($scope, $routeParams, trafficService, tenantService){
    $scope.cloudId = $routeParams.cloudId;
    $scope.id = $routeParams.id;
    $scope.traffic = {};

    trafficService.get($scope.id).then(function(response){
        $scope.traffic = response;
        $scope.getTenants();
    });

    $scope.tenants = [];
    $scope.getTenants = function(){
        tenantService.list($scope.cloudId).then(function(response){
            $scope.tenants = response;
            // Iterating through tenants to make radio button checked for matching tenant
            angular.forEach(response, function(tenant, i){
                if ($scope.traffic.tenants[0].tenant_id == tenant.tenant_id){
                    $scope.traffic.tenants[0] = tenant;
                }
            });
        });
    };

    $scope.selectTenant = function(tenant_id){
        trafficService.selectTenant($scope.traffic.id, tenant_id).then(function(response){
            console.log(response)
        });
    };

    $scope.selectNetwork = function(network_id, is_selected){
        trafficService.selectNetwork($scope.traffic.id, network_id, is_selected).then(function(response){
            console.log(response)
        });
    }
});


nttApp.controller('TrafficTestCtrl', function ($scope, $routeParams, trafficService) {
    $scope.id = $routeParams.id;
    $scope.cloudId = $routeParams.cloudId;
    $scope.showLoading = true;
    $scope.testResult = {};
    $scope.vmLaunchStatus = [];

    $scope.status = "Launching VM(s) on selected networks";
    trafficService.launchVM($scope.id).then(function(response){
        $scope.status = "Successfully launched VM(s) on selected networks"
        $scope.showLoading = false;
        $scope.vmLaunchStatus = response;
    });
});