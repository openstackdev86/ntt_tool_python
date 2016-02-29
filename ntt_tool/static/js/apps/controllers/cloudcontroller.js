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

    $scope.deleteTraffic = function($index){
        if(confirm("Are you sure want to delete?")) {
            cloudTrafficService.delete($scope.cloudTrafficList[$index].id).then(function (data) {
                $scope.cloudTrafficList.splice($index, 1);
            });
        }
    }
});



nttApp.controller('CloudTrafficCtrl', function($scope, $routeParams, $location, cloudService, cloudTrafficService){
    $scope.cloud = {};
    $scope.event = $routeParams.event;
    cloudService.get($routeParams.cloudId).then(function(data){
        $scope.cloud = data;
    });

    $scope.cloudTraffic = {};
    if($scope.event == 'edit'){
        cloudTrafficService.get($routeParams.trafficId).then(function(data){
            $scope.cloudTraffic = data;
        });
    };

    $scope.save = function(){
        if($scope.event == 'add') {
            $scope.cloudTraffic["cloud"] = $scope.cloud.id;
            cloudTrafficService.create($scope.cloudTraffic).then(function (data) {
                $location.path("cloudtraffic/view/" + data.id + "/");
            });
        }
        else{
            cloudTrafficService.update($scope.cloudTraffic.id, $scope.cloudTraffic).then(function (data) {
                $location.path("cloudtraffic/view/" + data.id + "/");
            });
        }
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

    $scope.tenantEvent = "Add";
    $scope.tenants = [];
    $scope.tenant = {};
    cloudTrafficTenantService.list($scope.cloudTrafficId).then(function(data){
       $scope.tenants = data;
    });

    $scope.addTenant = function(){
        $scope.tenantEvent = "Add";
        $scope.tenant["cloud_traffic_id"] = $scope.cloudTraffic.id;
        cloudTrafficTenantService.create($scope.tenant).then(function(data){
            $scope.tenants.push(data);
            $('#addTenantModal').modal('hide');
        });
    };

    $scope.editTenant = function($index){
        $scope.tenantEvent = "Edit";
        $scope.tenant = angular.copy($scope.tenants[$index]);
        cloudTrafficTenantService.update($scope.tenant.id, $scope.tenant).then(function(data){
            $scope.tenant[$index] = data;
            $('#addTenantModal').modal('hide');
        });
    };

    $scope.saveTenant = function(event, $index){
        cloudTrafficTenantService.save($scope.tenant).then(function(data){
            $scope.tenant = {};
            return data;
        });
    }

    $scope.deleteTenant = function($index){
        if(confirm("Are you sure you want to delete?")){
            cloudTrafficTenantService.delete($scope.tenants[$index].id).then(function(data){
               $scope.tenants.splice($index, 1);
            });
        }
    };

    $scope.saveExternalHost = function(){
        cloudTrafficService.update($scope.cloudTraffic.id, $scope.cloudTraffic).then(function (data) {
            $location.path("cloudtraffictest");
        });
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