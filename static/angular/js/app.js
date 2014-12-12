var StudentBaseApp = angular.module('AngularApp', [
    'ngRoute',
    'angularControllers',
    'angularServices',
]);

var configHttpProvider = function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
};

StudentBaseApp.config(['$httpProvider', configHttpProvider]);

StudentBaseApp.config(function($routeProvider, $locationProvider) {
    $routeProvider
    .when('/login', {
        templateUrl: vars.static_teampleate + 'login.html',
        controller: 'LoginCtrl'
    })
    .when('/logout', {
            templateUrl: vars.static_teampleate + 'logout.html',
        controller: 'LogoutCtrl'
    })
    .when('/groups', {
        templateUrl: vars.static_teampleate + 'group_list.html',
        controller: 'GroupList'
    })
    .when('/groups/:groupId', {
        templateUrl: vars.static_teampleate + 'student_list.html',
        controller: 'StudentList'
    })
    .when('/group_add', {
        templateUrl: vars.static_teampleate + 'group_add.html',
        controller: 'GroupAdd'
    })
    .when('/groups/edit/:groupId', {
        templateUrl: vars.static_teampleate + 'group_edit.html',
        controller: 'GroupEdit'
    })
    .when('/groups/delete/:groupId', {
        templateUrl: vars.static_teampleate + 'group_delete.html',
        controller: 'GroupDelete'
    })
    .when('/student_add', {
        templateUrl: vars.static_teampleate + 'student_add.html',
        controller: 'StudentAdd'
    })
    .when('/student/edit/:studentId', {
        templateUrl: vars.static_teampleate + 'student_edit.html',
        controller: 'StudentEdit'
    })
    .when('/student/delete/:studentId', {
        templateUrl: vars.static_teampleate + 'student_delete.html',
        controller: 'StudentDelete'
    })
    .otherwise({
        redirectTo:'/groups'
    });

    $locationProvider.html5Mode(true);
});

StudentBaseApp.directive('myLog', ['LoginService', function(LoginService) {

}]);