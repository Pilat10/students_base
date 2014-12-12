 var configHttpProvider = function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
};



var StudentBaseApp = angular.module('AngularApp', ['ngRoute']);

StudentBaseApp.config(['$httpProvider', configHttpProvider]);

StudentBaseApp.factory('LoginService', ['$http', function($http) {
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

StudentBaseApp.directive('myLog', ['LoginService', function(LoginService) {

}]);

StudentBaseApp.controller('MainController', function($scope, $route, $routeParams, $location, LoginService) {
    $scope.log = LoginService.isLogged()
    $scope.$route = $route;
    $scope.$location = $location;
    $scope.$routeParams = $routeParams;
});

StudentBaseApp.controller('LoginCtrl', function($scope, LoginService, $location){

    //$scope.loginn =
    LoginService.isLogged().success(function(data){
        //$scope.loginn = data;
        $location.path('/').replace();
    }).error(function(data){
        $scope.loginn = data;
    });
    $scope.submit = function(){
        LoginService.login($scope.user).success(function(data){
            //$scope.log_suc = data;
            $location.path('/').replace();
        }).error(function(data){
            $scope.error_data = true;
            //$scope.log_err = data;
            $scope.user = {
                username: "",
                password: ""
            };
        });


    };
});

StudentBaseApp.controller('LogoutCtrl', function($scope, LoginService, $location){
   LoginService.logout().success(function(){
       $location.path('/').replace();
   })
});

StudentBaseApp.controller('GroupList', function($scope, $http, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
    });

    $http.get('/api/v1/group/').success(function(data) {
        $scope.groups = data;
        $scope.show_group=false;
        if (data.status == "success"){
            $scope.show_group=true;
        }
        $scope.static = vars.static;
    })
});

StudentBaseApp.controller('StudentList', function($scope, $http, $routeParams) {
    $http.get('/api/v1/student/?group_id='+$routeParams.groupId)
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
    $http.get('/api/v1/group/'+ $routeParams.groupId +'/').success(function(data) {
        $scope.group = data.data;
        $http.get('/api/v1/student/?group_id='+$routeParams.groupId)
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
    $http.get('/api/v1/group/'+ $routeParams.groupId +'/').success(function(data) {
        $scope.group = data.data;
    });

    $scope.submit = function() {
        $http.delete('/api/v1/group/'+$routeParams.groupId+'/', $scope.group).success(function(data) {
                $location.path('/groups').replace();
            });

    };
});

StudentBaseApp.controller('StudentAdd', function($scope, $http, $location, $routeParams) {
    $http.get('/api/v1/group/').success(function(data){
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
        $http.post('/api/v1/student/', student).success(function(data){
            $location.path('/groups/'+$scope.student.group.id).replace();
        })
    };
});

StudentBaseApp.controller('StudentEdit', function($scope, $http, $location, $routeParams) {
    $http.get('/api/v1/student/'+ $routeParams.studentId +'/').success(function(data) {
        $scope.student = data.data;
        $scope.student.birthday = new Date($scope.student.birthday);
        $http.get('/api/v1/group/').success(function(data) {
            $scope.groups = data.data;
            for(var i = 0; i<$scope.groups.length; i++){
                if($scope.groups[i].id == $scope.student.group){
                    $scope.student.group = $scope.groups[i];
                }
            }
        })
    });

    $scope.submit = function() {
        var date = $scope.student.birthday;
        var student = {
            fio: $scope.student.fio,
            birthday: date.getFullYear().toString()+'-'+(date.getMonth()+1).toString()+'-'+date.getDate().toString(),
            number_student_cart: $scope.student.number_student_cart,
            group: $scope.student.group.id
        }
        $http.put('/api/v1/student/'+$routeParams.studentId, student)
        .success(function(data) {
            $location.path('/groups/'+$scope.student.group.id).replace();
        });
    };
});

StudentBaseApp.controller('StudentDelete', function($scope, $http, $location, $routeParams) {
    $http.get('/api/v1/student/'+ $routeParams.studentId +'/').success(function(data) {
        $scope.student = data.data;
    });

    $scope.submit = function() {
        $http.delete('/api/v1/student/'+$routeParams.studentId+'/', $scope.student).success(function(data) {
            $location.path('/groups/'+$scope.student.group).replace();
        });

    };
});