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
StudentBaseApp.config(['$httpProvider', configHttpProvider]);

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

StudentBaseApp.controller('GroupList', function($scope, $http) {
    $http.get('/api/v1/group/.json').success(function(data) {
        $scope.groups = data;
        $scope.show_group=false;
        if (data.status == "success"){
            $scope.show_group=true;
        }
        $scope.static = vars.static;
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
            $scope.group_id = $routeParams.groupId
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
                    $scope.group.headman = $scope.students[i];
                }
            }
        })
    });

    $scope.submit = function() {
        if ($scope.group.name) {
            if($scope.group.headman != null){
                $scope.group.headman = $scope.group.headman.id;
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
        $http.delete('/api/v1/group/'+$routeParams.groupId+'/', $scope.group).success(function(data) {
                $location.path('/groups').replace();
            });

    };
});

StudentBaseApp.controller('StudentAdd', function($scope, $http, $location, $routeParams) {
    $http.get('/api/v1/group/.json').success(function(data){
        $scope.groups = data.data;
    })
    $scope.group_id = $routeParams.group_id;
    $scope.submit = function() {
        var date = $scope.student.birthday;
        var student = {
            fio: $scope.student.fio,
            birthday: date.getFullYear().toString()+'-'+(date.getMonth()+1).toString()+'-'+date.getDate().toString(),
            number_student_cart: $scope.student.number_student_cart,
            group: $scope.student.group.id
        }
        $http.post('/api/v1/students/', student).success(function(data){
            $location.path('/groups/'+$scope.student.group.id).replace();
        })
    };
});

StudentBaseApp.controller('StudentEdit', function($scope, $http, $location, $routeParams) {
    $http.get('/api/v1/students/'+ $routeParams.studentId +'/.json').success(function(data) {
        $scope.student = data.data;
        $scope.student.birthday = new Date($scope.student.birthday);
        $http.get('/api/v1/group/.json').success(function(data) {
            $scope.groups = data.data;
            for(var i = 0; i<$scope.groups.length; i++){
                if($scope.groups[i].id == $scope.student.group){
                    $scope.student.group = $scope.groups[i];
                }
            }
        })
    });

    $scope.fffd='dfds';
    $scope.submit = function() {
        var date = $scope.student.birthday;
        var student = {
            fio: $scope.student.fio,
            birthday: date.getFullYear().toString()+'-'+(date.getMonth()+1).toString()+'-'+date.getDate().toString(),
            number_student_cart: $scope.student.number_student_cart,
            group: $scope.student.group.id
        }
        $http.put('/api/v1/students/'+$routeParams.studentId, student)
        .success(function(data) {
            $location.path('/groups/'+$scope.student.group.id).replace();
        });
    };
});

StudentBaseApp.controller('StudentDelete', function($scope, $http, $location, $routeParams) {
    $http.get('/api/v1/students/'+ $routeParams.studentId +'/.json').success(function(data) {
        $scope.student = data.data;
    });

    $scope.submit = function() {
        $http.delete('/api/v1/students/'+$routeParams.studentId+'/', $scope.student).success(function(data) {
            $location.path('/groups/'+$scope.student.group).replace();
        });

    };
});