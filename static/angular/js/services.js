'use strict';

/* Services */

var angularServices = angular.module('angularServices', []);

angularServices.factory('LoginService', ['$http', function($http) {
    return {
        apiBase: '/api/v1/auth/',
        http: $http,
        userService: "userService",
        isLogged: function(){
            return this.http.get(this.apiBase);
        },
        login: function(user){
            return this.http.post(this.apiBase, user);
        },
        logout: function(){
            return this.http.delete(this.apiBase);
        }
    }
}]);
