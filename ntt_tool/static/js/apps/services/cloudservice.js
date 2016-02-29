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
        console.log(params)
        return dataService.post2('/api/cloud/'+pk+'/', params);
    };
    this.delete = function(id){
        return dataService.delete('/api/cloud/'+id+'/');
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
    this.update = function(params){
        return dataService.update('/api/cloudtraffic/', params);
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