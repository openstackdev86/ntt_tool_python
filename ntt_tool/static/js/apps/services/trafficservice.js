nttApp.service('trafficService', function(dataService){
    this.list = function(cloudId){
        return dataService.get('/api/traffic/?cloud_id=' + cloudId);
    };

    this.get = function(pk) {
        return dataService.get('/api/traffic/' + pk + '/');
    };

    this.create = function(params){
        return dataService.post('/api/traffic/', params);
    };

    this.update = function(pk, params){
        return dataService.put('/api/traffic/'+pk+'/', params);
    };

    this.delete = function(pk){
        return dataService.delete('/api/traffic/'+pk+'/');
    };

    this.selectTenant = function(pk, tenantId){
        return dataService.get('/api/traffic/' + pk + '/select/tenant/' + tenantId + '/');
    };

    this.selectNetwork = function(pk, params){
        return dataService.get('/api/traffic/' + pk + '/select/network/?'+$.param(params));
    };

    this.endpoints = function(pk){
        return dataService.get('/api/traffic/' + pk + '/endpoints/');
    };

    this.discoverEndpoints = function(pk, params){
        return dataService.postJSON('/api/traffic/' +pk + '/endpoints/discover/', params);
    };
1
    this.launchEndpoints = function(pk, params) {
        return dataService.postJSON('/api/traffic/' +pk + '/endpoints/launch/', params);
    };

    this.selectEndpoint = function (pk, params) {
        return dataService.get('/api/traffic/' +pk + '/endpoints/select/?'+$.param(params));
    };

    this.runTrafficTest = function(pk){
        return dataService.get('/api/traffic/' + pk + '/run/test/');
    };
});






