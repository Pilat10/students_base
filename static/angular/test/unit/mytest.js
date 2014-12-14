'use strict';
git
describe('Test LoginService', function(){

    var LoginService;
    beforeEach(module('angularApp'));
    beforeEach(inject(function($injector){
        LoginService = $injector.get('LoginService')
    }));

    it('my test service', function() {
        expect(LoginService).toBeDefined();
    });

    it('', function () {
       expect(LoginService.apiBase).toBe('/api/v1/auth/')
    });
});