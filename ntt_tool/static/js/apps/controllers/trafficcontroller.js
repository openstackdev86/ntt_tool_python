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
    $scope.cloudTraffic = {
        "cloud_id": $scope.cloudId,
        "tenant_type": "all",
        "test_method": "icmp",
        "tenants": [],
    };

    if ($scope.event == "edit"){
        trafficService.get($scope.id).then(function(response){
            $scope.cloudTraffic = response;
            $scope.getTenants();
        });
    }

    $scope.tenants = [];
    $scope.getTenants = function(){
        tenantService.list($scope.cloudId).then(function(response){
            if ($scope.event == 'add'){
                $scope.tenants = response;
            }
            else {
                angular.forEach(response, function(tenant, i){
                    var isSelected = false;
                    angular.forEach($scope.cloudTraffic.tenants, function(selectedTenant, j){
                        if (tenant.tenant_name == selectedTenant.tenant_name){
                            isSelected = true;
                        }
                    });
                    if (!isSelected){
                        $scope.tenants.push(tenant);
                    }
                });
            }
        });
    };
    if($scope.event == 'add'){
        $scope.getTenants();
    }

    $scope.selectTenant = function($index){
        var selectedTenant = angular.copy($scope.tenants[$index]);
        $scope.tenants.splice($index, 1);
        $scope.cloudTraffic.tenants.push(selectedTenant);
    };

    $scope.unSelectTenant = function($index){
        var unselectedTenant = angular.copy($scope.cloudTraffic.tenants[$index]);
        $scope.cloudTraffic.tenants.splice($index, 1);
        $scope.tenants.push(unselectedTenant);
    };

    $scope.getSelectedTenants = function(){
        var selectedList = [];
        angular.forEach($scope.cloudTraffic.tenants, function(item, index){
            selectedList.push(item.id);
        });
        console.log(selectedList)
        return selectedList;
    };

    $scope.save = function(){
        if($scope.event == "add") {
            $scope.cloudTraffic["tenants"] = $scope.getSelectedTenants()
            trafficService.create($scope.cloudTraffic).then(function (response) {
                $location.path("cloud/view/" + $scope.cloudId + "/");
            });
        }
        else {
            trafficService.update($scope.cloudTraffic.id, $scope.cloudTraffic).then(function(response){
                $location.path("cloud/view/" + $scope.cloudId + "/");
            });
        }
    };
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