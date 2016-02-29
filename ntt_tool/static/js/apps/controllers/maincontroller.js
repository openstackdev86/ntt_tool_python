nttApp.controller('IndexCtrl', function($rootScope, $scope, $location){
    if($rootScope.isLoggedin){
        $location.path('clouds');
    }
});

nttApp.controller('DashboardCtrl', function($scope){
    $scope.msg = "You are at dashboard page";
});