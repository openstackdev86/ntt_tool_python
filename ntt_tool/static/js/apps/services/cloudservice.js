nttApp.service('cloudService', function(dataService){
    this.list = function(){
        return dataService.get('/api/cloud/');
    };
    this.get = function(id){
        return dataService.get('/api/cloud/'+id+'/');
    };
    this.create = function(params){
        return dataService.post('/api/cloud/', params);
    };
    this.update = function(pk, params){
        return dataService.put('/api/cloud/'+pk+'/', params);
    };
    this.delete = function(pk){
        return dataService.delete('/api/cloud/'+pk+'/');
    };
});

