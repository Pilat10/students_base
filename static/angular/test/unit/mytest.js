'use strict';

describe('Test LoginService', function(){

    var LoginService, $httpBackend;
    beforeEach(module('angularApp'));
    beforeEach(inject(function($injector, _$httpBackend_){
        LoginService = $injector.get('LoginService');
        $httpBackend = _$httpBackend_;
        $httpBackend.expectGET('/api/v1/auth/').respond([{
            "status": "success",
            "data": {
                "user": "admin",
                "auth": "None"
            }
        }]);
    }));

    it('my test service', function() {
        expect(LoginService).toBeDefined();
    });

    it('my test', function() {

        //$httpBackend.flush();
        LoginService.isLogged().success(function(data){
            expect(data).toEqual([{
            "status": "success",
            "data": {
                "user": "admin",
                "auth": "None"
            }
        }]);
        }).error(function(data){
            expect(data).toEqual('dfds');
        });
        $httpBackend.flush();
        //expect(LoginService.login()).toEqual('dfds')
    });

    it('', function () {
       expect(LoginService.apiBase).toBe('/api/v1/auth/')
    });
});