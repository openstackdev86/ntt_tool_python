nttApp.service('tenantService', function (dataService) {
    this.discover = function(cloudId){
        return dataService.get('/api/tenant/discover/' + cloudId + '/');
    };

    this.list = function(cloudId){
        return dataService.get('/api/tenant/?cloud_id='+cloudId);
    };

    this.save = function(params){
        return dataService.post('/api/tenant/', params);
    };
});


