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
        "tenant_type": "intra-tenant",
        "test_method": "icmp",
        "tenant": {},
    };

    if ($scope.event == "edit"){
        trafficService.get($scope.id).then(function(response){
            console.log(response);
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
                $scope.tenants = response;
                // Iterating through tenants to make radio button checked for matching tenant
                angular.forEach(response, function(tenant, i){
                    if ($scope.cloudTraffic.tenants[0].tenant_id == tenant.tenant_id){
                        $scope.cloudTraffic.tenants[0] = tenant;
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



    $scope.selectedTenant = {};
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