nttApp.controller('TrafficListCtrl', function($scope, trafficService){

});

nttApp.controller('TrafficCtrl', function($scope, $routeParams, trafficService){
    $scope.cloudId = $routeParams.cloudId;
    $scope.event = $scope.id == undefined ? "add" : "edit";
    $scope.traffic = {};
});