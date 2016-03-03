nttApp.controller('IndexCtrl', function($rootScope, $scope, $location){
    if($rootScope.isLoggedin){
        $location.path('cloud');
    }
});

nttApp.controller('DashboardCtrl', function($scope){
    $scope.msg = "You are at dashboard page";
});