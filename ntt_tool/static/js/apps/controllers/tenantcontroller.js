nttApp.controller('TenantListCtrl', function($scope, $routeParams, tenantService){
    $scope.cloudId = $routeParams.id;
    $scope.tenants = [];
    tenantService.list($scope.cloudId).then(function(response){
        $scope.tenants = response;
    });
});

nttApp.controller('TenantDiscoveryCtrl', function($scope, $routeParams, tenantService){
    $scope.cloudId = $routeParams.cloudId;
    $scope.discoveryResult = {};

    $scope.showLoading = true;
    $scope.discover = function(){
        tenantService.discover($scope.cloudId).then(function(response){
            $scope.showLoading = false;
            $scope.discoveryResult = response;
        });
    };
    $scope.discover();
});