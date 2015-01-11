'use strict';

/* Derectives */

var angularDirectives = angular.module('angularDirectives', []);

angularDirectives.directive('navbar', function() {
    return {
        templateUrl: vars.static_teampleate + 'navigation_bar.html',
        scope: true
    };
});