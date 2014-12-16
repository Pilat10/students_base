vars = {
    static: '/static/',
    static_teampleate: '/static/angular/views/'
}

var StudentBaseApp = angular.module('angularApp', [
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
    .when('/' , {
        templateUrl: vars.static_teampleate + 'home.html',
        controller: 'HomeCtrl'
    })
    .when('/login', {
        templateUrl: vars.static_teampleate + 'login.html',
        controller: 'LoginCtrl'
    })
    .when('/logout', {
        templateUrl: vars.static_teampleate + 'logout.html',
        controller: 'LogoutCtrl'
    })
    .when('/departments', {
        templateUrl: vars.static_teampleate + 'department_list.html',
        controller: 'DepartmentListCtrl'
    })
    .when('/departments/:departmentId', {
        templateUrl: vars.static_teampleate + 'group_list.html',
        controller: 'GroupList'
    })
    .when('/department/add', {
        templateUrl: vars.static_teampleate + 'department_add.html',
        controller: 'DepartmentAddCtrl'
    })
    .when('/department/edit/:departmentId', {
        templateUrl: vars.static_teampleate + 'department_edit.html',
        controller: 'DepartmentEditCtrl'
    })
    .when('/department/delete/:departmentId', {
        templateUrl: vars.static_teampleate + 'department_delete.html',
        controller: 'DepartmentDeleteCtrl'
    })
    .when('/groups', {
        templateUrl: vars.static_teampleate + 'group_list.html',
        controller: 'GroupList'
    })
    .when('/groups/:groupId', {
        templateUrl: vars.static_teampleate + 'student_list.html',
        controller: 'StudentList'
    })
    .when('/group/add', {
        templateUrl: vars.static_teampleate + 'group_add.html',
        controller: 'GroupAdd'
    })
    .when('/group/edit/:groupId', {
        templateUrl: vars.static_teampleate + 'group_edit.html',
        controller: 'GroupEdit'
    })
    .when('/group/delete/:groupId', {
        templateUrl: vars.static_teampleate + 'group_delete.html',
        controller: 'GroupDelete'
    })
    .when('/students', {
        templateUrl: vars.static_teampleate + 'student_list.html',
        controller: 'StudentList'
    })
    .when('/student/add', {
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
        redirectTo:'/'
    });

    $locationProvider.html5Mode(true);
});

StudentBaseApp.directive('navbar', function() {
    return {
        templateUrl: vars.static_teampleate + 'navigation_bar.html'
    };
});