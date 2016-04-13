nttApp.controller('TenantListCtrl', function($scope, $routeParams, tenantService){
    $scope.cloudId = $routeParams.id;
    $scope.tenants = [];
    tenantService.list($scope.cloudId).then(function(response){
        $scope.tenants = response;
    });

    $scope.showLoading = false;
    $scope.discover = function(){
        $scope.showLoading = true;
        tenantService.discover($scope.cloudId).then(function(response){
            $scope.showLoading = false;
            $scope.tenants = response;
        });
    };
});