'use strict';

describe("Testing Modules", function(){
    describe("App Module:", function(){
        var module;
        beforeEach(function(){
            module = angular.module("angularApp")
        });

        it("should be registred", function(){
            expect(module).not.toBeNull();
        });

        describe("Dependencies:", function() {

            var deps;
            var hasModule = function(m) {
                return deps.indexOf(m) >= 0;
            };
            beforeEach(function() {
                deps = module.value('appName').requires;
            });

            it("should have ngRoute as a dependency", function() {
                expect(hasModule('ngRoute')).toEqual(true);
            });

            it("should have angularControllers as a dependency", function() {
                expect(hasModule('angularControllers')).toEqual(true);
            });

            it("should have angularDirectives as a dependency", function() {
                expect(hasModule('angularDirectives')).toEqual(true);
            });

            it("should have angularServices as a dependency", function() {
                expect(hasModule('angularServices')).toEqual(true);
            });
        });
    });
});