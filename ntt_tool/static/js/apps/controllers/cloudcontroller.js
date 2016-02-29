nttApp.controller('CloudsCtrl', function($scope, cloudService){
    $scope.clouds = [];
    $scope.getClouds = function(){
        cloudService.list().then(function(data){
            $scope.clouds = data;
        })
    };
    $scope.getClouds();

    $scope.delete = function($index){
        if(confirm("Are you sure want to delete?")){
            cloudService.delete($scope.clouds[$index].id).then(function(data){
               $scope.clouds.splice($index, 1);
            });
        }
    };
});


nttApp.controller('CloudCtrl', function($scope, $routeParams, $location, cloudService, cloudTrafficService){
    $scope.cloudId = $routeParams.cloudId;
    $scope.event = $routeParams.event;
    $scope.cloud = {};
    $scope.cloudTrafficList = [];

    if ($scope.cloudId != undefined){
        cloudService.get($scope.cloudId).then(function(data){
            $scope.cloud = data;
        });

        cloudTrafficService.list($scope.cloudId).then(function (data) {
            $scope.cloudTrafficList = data;
        })
    };

    $scope.save = function(){
        if ($scope.event == 'add'){
            cloudService.create($scope.cloud).then(function (data) {
                $location.path("cloudtraffic/add/"+ data.id +"/");
            });
        }
        else {
            cloudService.update($scope.cloud.id, $scope.cloud).then(function(data){
               $location.path("cloud/"+$scope.cloud.id+"/");
            });
        };

    };
});



nttApp.controller('CloudTrafficCtrl', function($scope, $routeParams, $location, cloudService, cloudTrafficService){
    $scope.cloud = {};
    cloudService.get($routeParams.cloudId).then(function(data){
        $scope.cloud = data;
    });

    $scope.cloudTraffic = {};
    $scope.save = function(){
        $scope.cloudTraffic["cloud"] = $scope.cloud.id;
        cloudTrafficService.create($scope.cloudTraffic).then(function (data) {
            $location.path("cloudtraffic/view/"+ data.id +"/");
        });
    };
});

nttApp.controller('CloudTrafficViewCtrl', function($scope, $routeParams, $location, cloudService, cloudTrafficService, cloudTrafficTenantService){
    $scope.cloud = {};
    $scope.cloudTrafficId = $routeParams.id;
    $scope.cloudTraffic = {};

    cloudTrafficService.get($scope.cloudTrafficId).then(function(data){
        $scope.cloudTraffic = data;
        $scope.getCloud($scope.cloudTraffic.cloud);
    });

    $scope.getCloud = function(cloudId){
        cloudService.get(cloudId).then(function(data){
            $scope.cloud = data;
        });
    }

    $scope.tenants = [];
    $scope.tenant = {};
    cloudTrafficTenantService.list($scope.cloudTrafficId).then(function(data){
       $scope.tenants = data;
    });

    $scope.addTenant = function(){
        $scope.tenant["cloud_traffic_id"] = $scope.cloudTraffic.id;
        cloudTrafficTenantService.save($scope.tenant).then(function(data){
            $scope.tenant = {};
            $scope.tenants.push(data);
            $('#addTenantModal').modal('hide');
        });
    };

    $scope.saveExternalHost = function(){
        //cloudTrafficService.update($scope.cloudTraffic).then(function (data) {
            $location.path("cloudtraffictest");
        //});
    };
});

nttApp.controller('CloudTrafficTestCtrl', function($scope, $location, cloudTrafficService){

});

//nttApp.controller('CloudTrafficTenantsCtrl', function ($scope, $routeParams, $location, CloudTrafficTenantService) {
//    $scope.trafficId = $routeParams.trafficId;
//    $scope.tenants = {};
//
//    $scope.save = function(){
//        $scope.tenants["cloud_traffic"] = $scope.trafficId;
//        CloudTrafficTenantService.save($scope.tenants).then(function (data) {
//            $location.path("cloudtraffictenants/sshgateway/"+ data.id +"/");
//        });
//    };
//});
//
//
//nttApp.controller('cloudTrafficTenantsSSHGatewayCtrl', function($scope, $routeParams, $location){
//    $scope.trafficId = $routeParams.trafficId;
//    $scope.tenants = {};
//
//    CloudTrafficTenantService.list($scope.trafficId).then(function(data){
//        $scope.tenants = data;
//    });
//});