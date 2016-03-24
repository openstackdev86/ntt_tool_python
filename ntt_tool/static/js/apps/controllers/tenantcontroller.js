nttApp.controller('TenantListCtrl', function($scope, $routeParams, tenantService){
    $scope.cloudId = $routeParams.id;
    $scope.tenants = [];
    tenantService.list($scope.cloudId).then(function(response){
        $scope.tenants = response;
    });

    $scope.showLoading = true;
    $scope.discover = function(){
        $scope.showLoading = true;
        tenantService.discover($scope.cloudId).then(function(response){
            $scope.showLoading = false;
            $scope.tenants = response;
        });
    };
});

//nttApp.controller('TenantDiscoveryCtrl', function($scope, $routeParams, tenantService){
//    console.log($routeParams)
//    $scope.cloudId = $routeParams.id;
//    $scope.discoveryResult = {};
//    console.log("1")
//    $scope.showLoading = true;
//    $scope.discover = function(){
//        console.log("2")
//        tenantService.discover($scope.cloudId).then(function(response){
//            console.log("3")
//            $scope.showLoading = false;
//            $scope.discoveryResult = response;
//        });
//    };
//    $scope.discover();
//});