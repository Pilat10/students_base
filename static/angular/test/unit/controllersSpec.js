'use strict';

describe('Angular controllers', function(){

    beforeEach(module('angularApp'));
    beforeEach(module('angularControllers'));

    describe('DepartmentListCtrl', function(){
        var scope, ctrl, $httpBackend;

        beforeEach(inject(function(_$httpBackend_, $rootScope, $controller) {
            $httpBackend = _$httpBackend_;
            $httpBackend.expectGET('/api/v1/auth/').respond({"status": "success", "data": {"user": "admin", "auth": "None"}});
            $httpBackend.expectGET('/api/v1/department/').respond({"status": "success", "data": [{"id": 1, "name_department": "Dep 1", "count_group": 3, "count_student": 17, "avg_age": 3.0588235294117645}, {"id": 2, "name_department": "Dep 2", "count_group": 1, "count_student": 5, "avg_age": 22.0} ]});
            scope = $rootScope.$new();
            ctrl = $controller('DepartmentListCtrl', {$scope: scope});
        }));

        it('Get department', function(){
            expect(scope.departments).not.toBeDefined();
            $httpBackend.flush();
            expect(scope.user).toBe('admin')
            expect(scope.departments).toEqual(
                {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "name_department": "Dep 1",
                        "count_group": 3,
                        "count_student": 17,
                        "avg_age": 3.0588235294117645
                    },
                    {
                        "id": 2,
                        "name_department": "Dep 2",
                        "count_group": 1,
                        "count_student": 5,
                        "avg_age": 22.0
                    }
                ]
            });
            expect(true).toBe(true);
        });

    });



});