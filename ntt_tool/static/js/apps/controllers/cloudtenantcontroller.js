nttApp.controller('CloudTenantListCtrl', function($scope){
    $scope.tenantList = [
        {'id':1, 'name':'Name 1', 'ip':'ip'},
        {'id':1, 'name':'Name 1', 'ip':'ip'}
    ];
});

nttApp.controller('CloudTenantDiscoveryCtrl', function($scope, $routeParams, cloudTenantService){
    $scope.cloudId = $routeParams.cloudId;
    $scope.tenantList = [];

    $scope.discover = function(){
        cloudTenantService.discover($scope.cloudId).then(function(data){
            console.log(data);
        });
    };
    $scope.discover();
});