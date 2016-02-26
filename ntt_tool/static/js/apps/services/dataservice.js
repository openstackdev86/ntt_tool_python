'use strict';

nttApp.service('dataService', ['$http', '$q', function ($http, $q) {
    this.get = function (url) {
        var deferred = $q.defer();
        var request = $http.get(url);
        request.success(function (data, status, headers, config) {
            deferred.resolve(data);
        });
        request.error(function (data, status) {
            deferred.reject(data);
        });
        return deferred.promise;
    };

    this.post = function (url, params) {
        var deferred = $q.defer();
        var request = $http({
            method: "post",
            url: url,
            data: $.param(params)
        });
        request.success(function (data, status, headers, config) {
            deferred.resolve(data)
        });
        request.error(function (response) {
            deferred.reject(response);
        });
        return deferred.promise;
    };

    this.update = function (url, params) {
        var deferred = $q.defer();
        var request = $http({
            method: "patch",
            url: url,
            data: $.param(params)
        });
        request.success(function (data, status, headers, config) {
            deferred.resolve(data)
        });
        request.error(function (response) {
            deferred.reject(response);
        });
        return deferred.promise;
    };
}]);