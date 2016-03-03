nttApp.service('cloudTenantService', function (dataService) {
   this.discover = function(cloudId){
       return dataService.get('/api/cloudtenants/discover/' + cloudId + '/');
   }
});



//
//nttApp.service('cloudTrafficTenantService', function(dataService){
//    this.list = function(trafficId){
//        return dataService.get('/api/cloudtraffictenant/?traffic_id='+trafficId);
//    };
//    this.get = function(trafficId) {
//        return dataService.get('/api/cloudtraffictenant/'+trafficId+'/');
//    };
//    this.create = function(params){
//        return dataService.post('/api/cloudtraffictenant/', params);
//    };
//    this.update = function(pk, params){
//        return dataService.put('/api/cloudtraffictenant/'+pk+'/', params);
//    };
//    this.delete = function(pk){
//        return dataService.delete('/api/cloudtraffictenant/'+pk+'/');
//    };
//});