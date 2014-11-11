 var configHttpProvider = function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
};



var StudentBaseApp = angular.module('AngularApp', ['ngRoute']);

StudentBaseApp.controller('MainController', function($scope, $route, $routeParams, $location) {
     $scope.$route = $route;
     $scope.$location = $location;
     $scope.$routeParams = $routeParams;
});

 StudentBaseApp.controller('BookController', function($scope, $routeParams) {
     $scope.name = "BookController";
     $scope.params = $routeParams;
 });



















StudentBaseApp.config(['$httpProvider', configHttpProvider]);

StudentBaseApp.config(function($interpolateProvider, $locationProvider) {
    //$interpolateProvider.startSymbol('{$');
    //$interpolateProvider.endSymbol('$}');
});

StudentBaseApp.config(function($routeProvider, $locationProvider) {
    $routeProvider
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
    .otherwise({
        //templateUrl: '/static/angular/book.html',
        //controller: 'BookController'
        //redirectTo:'/groups'
    });

    // configure html5 to get links working on jsfiddle
    $locationProvider.html5Mode(true);
});

StudentBaseApp.controller('GroupList', function($scope, $http) {
    $http.get('/api/v1/group/.json').success(function(data) {
        $scope.groups = data;
        $scope.show_group=false;
        if (data.status == "success"){
            $scope.show_group=true;
        }
        $scope.static = vars.static;
        $scope.sss = vars.static + 'group_list.html';
    })
});

StudentBaseApp.controller('StudentList', function($scope, $http, $routeParams) {
    $http.get('/api/v1/students/.json?group_id='+$routeParams.groupId)
        .success(function(data) {
            $scope.students = data;
            $scope.show_students=false;
            if (data.status == "success"){
                $scope.show_students=true;
            }
            $scope.static = vars.static;
    })
});

StudentBaseApp.controller('GroupAdd', function($scope, $http, $location) {
    $scope.submit = function() {
        if ($scope.group.name) {
            $scope.group.headman = '';
            $http.post('/api/v1/group/', $scope.group)
            .success(function(data) {
                $location.path('/groups').replace();
            });
        }
    };
});

StudentBaseApp.controller('GroupEdit', function($scope, $http, $location, $routeParams) {
    $http.get('/api/v1/group/'+ $routeParams.groupId +'/.json').success(function(data) {
        $scope.group = data.data;
        $http.get('/api/v1/students/.json?group_id='+$routeParams.groupId)
        .success(function(data) {
            $scope.students = data.data;
            for(var i = 0; i<$scope.students.length; i++){
                if($scope.students[i].id == $scope.group.headman){
                    $scope.MyStud = $scope.students[i];
                }
            }
        })
    });

    $scope.submit = function() {
        if ($scope.group.name) {
            if($scope.MyStud != null){
                $scope.group.headman = $scope.MyStud.id;
            } else {
                $scope.group.headman = '';
            }

            $http.put('/api/v1/group/'+$routeParams.groupId, $scope.group)
            .success(function(data) {
                $location.path('/groups').replace();
            });
        }
    };
});

StudentBaseApp.controller('GroupDelete', function($scope, $http, $location, $routeParams) {
    $http.get('/api/v1/group/'+ $routeParams.groupId +'/.json').success(function(data) {
        $scope.group = data.data;
    });

    $scope.submit = function() {
        $http.delete('/api/v1/group/'+$routeParams.groupId, $scope.group).success(function(data) {
                $location.path('/groups').replace();
            });

    };
});
