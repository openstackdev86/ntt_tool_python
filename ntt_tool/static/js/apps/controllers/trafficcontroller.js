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


nttApp.controller('TrafficCtrl', function($scope, $routeParams, $location, trafficService){
    $scope.cloudId = $routeParams.cloudId;
    $scope.id = $routeParams.id;
    $scope.event = $scope.id == undefined ? "add" : "edit";
    $scope.cloudTraffic = {
        "cloud_id": $scope.cloudId,
        "tenant_type": "all",
        "test_method": "icmp"
    };

    if ($scope.event == "edit"){
        trafficService.get($scope.id).then(function(response){
           $scope.cloudTraffic = response;
        });
    }

    $scope.selectTenant = function($index){
        var selectedTenant = angular.copy($scope.cloudTraffic.available_tenants[$index]);
        $scope.cloudTraffic.available_tenants.splice($index, 1);
        $scope.cloudTraffic.selected_tenants.push(selectedTenant);
    };
    $scope.unSelectTenant = function($index){
        var unselectedTenant = angular.copy($scope.cloudTraffic.selected_tenants[$index]);
        $scope.cloudTraffic.selected_tenants.splice($index, 1);
        $scope.cloudTraffic.available_tenants.push(unselectedTenant);
    };
    $scope.getSelectedTenants = function(){
        var selectedList = [];
        angular.forEach($scope.cloudTraffic.selected_tenants, function(item, index){
            selectedList.push(item.id);
        });
        return selectedList;
    };

    $scope.save = function(){
        $scope.cloudTraffic["tenants"] = $scope.getSelectedTenants();
        if($scope.event == "add") {
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

    trafficService.test($scope.id).then(function(response){
        console.log(response);
    });
});