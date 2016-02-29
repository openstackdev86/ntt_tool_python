nttApp.service('cloudService', function(dataService){
    this.list = function(){
        return dataService.get('/api/cloud/');
    };
    this.get = function(id){
        return dataService.get('/api/cloud/'+id+'/');
    };
    this.create = function(params){
        return dataService.post('/api/cloud/1/', params);
    };
    this.update = function(pk, params){
        return dataService.put('/api/cloud/'+pk+'/', params);
    };
    this.delete = function(pk){
        return dataService.delete('/api/cloud/'+pk+'/');
    };
});

nttApp.service('cloudTrafficService', function(dataService){
    this.list = function(cloudId){
        return dataService.get('/api/cloudtraffics/'+cloudId+'/');
    };
    this.get = function(id){
        return dataService.get('/api/cloudtraffic/'+id+'/');
    };
    this.create = function(params){
        return dataService.post('/api/cloudtraffic/', params);
    };
    this.update = function(pk, params){
        return dataService.put('/api/cloudtraffic/'+pk+'/', params);
    };
    this.delete = function(pk){
        return dataService.delete('/api/cloudtraffic/'+pk+'/');
    };
});

nttApp.service('cloudTrafficTenantService', function(dataService){
    this.list = function(trafficId){
        return dataService.get('/api/cloudtraffictenants/'+trafficId+'/');
    };
    this.get = function(trafficId) {
        return dataService.get('/api/cloudtraffictenant/'+trafficId+'/');
    };
    this.save = function(params){
        return dataService.post('/api/cloudtraffictenant/', params);
    };
});