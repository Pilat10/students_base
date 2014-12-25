'use strict';

/* Controllers */

var angularControllers = angular.module('angularControllers', []);

angularControllers.controller('MainController', function($scope, $route, $routeParams, $location, LoginService) {
    $scope.test = false;
    $scope.$route = $route;
    $scope.$location = $location;
    $scope.$routeParams = $routeParams;
    $scope.depId = '';
    $scope.groupIdMain = '';
    $scope.setDepId = function(depId) {
        $scope.depId = depId;
    };
    $scope.setGroupId = function(groupIdMain) {
        $scope.groupIdMain = groupIdMain;
    };
});

angularControllers.controller('HomeCtrl', function($scope, $http, $location, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
    });
});

angularControllers.controller('LoginCtrl', function($scope, LoginService, $location){

    LoginService.isLogged().success(function(data){
        $location.path('/').replace();
    }).error(function(data){
        $scope.loginn = data;
    });
    $scope.submit = function(){
        LoginService.login($scope.user).success(function(data){
            $location.path('/').replace();
        }).error(function(data){
            $scope.error_data = true;
            $scope.user = {
                username: "",
                password: ""
            };
        });
    };
});

angularControllers.controller('LogoutCtrl', function($scope, LoginService, $location){
   LoginService.logout().success(function(){
       $location.path('/').replace();
   })
});

angularControllers.controller('DepartmentListCtrl', function($scope, $http, $location, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
    });
    $http.get('/api/v1/department/').success(function(data){
        $scope.departments = data;
    });
    $scope.addButton = function(){
        if($scope.logged){
            $location.path('department/add').replace();
        } else {
            $scope.notLoggedMsg = true;
        }
    };
    $scope.editButton = function(dep_id){
        if($scope.logged){
            $location.path('department/edit/'+dep_id+'/').replace();
        } else {
            $scope.notLoggedMsg = true;
        }
    };
    $scope.deleteButton = function(dep_id){
        if($scope.logged){
            $location.path('department/delete/'+dep_id+'/').replace();
        } else {
            $scope.notLoggedMsg = true;
        }
    };
});

angularControllers.controller('DepartmentAddCtrl', function($scope, $http, $location, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
        $location.path('/departments').replace();
    });
    $scope.department = {
        "name_department": ""
    }
    $scope.submit = function(){
        if ($scope.department.name_department){
            $http.post('/api/v1/department/', $scope.department).success(function(){
                $location.path('/departments').replace();
            }).error(function(){
                $scope.error = "Error";
            });
        } else {
            $scope.error = "Name department field is required!!!"
        }
    };
});

angularControllers.controller('DepartmentEditCtrl', function($scope, $http, $location, $routeParams, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
        $location.path('/departments').replace();
    });
    $http.get('/api/v1/department/'+$routeParams.departmentId+'/').success(function(data){
        $scope.department = data.data;
    });
    $scope.submit = function(){
        if ($scope.department.name_department){
            var department = {
                "name_department": $scope.name_department
            }
            $http.put('/api/v1/department/'+$routeParams.departmentId+'/', $scope.department).success(function(){
                $location.path('/departments').replace();
            }).error(function(){
                $scope.error = "Error";
            });
        } else {
            $scope.error = "Name department field is required!!!"
        }
    };
});

angularControllers.controller('DepartmentDeleteCtrl', function($scope, $http, $location, $routeParams, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
        $location.path('/departments').replace();
    });
    $http.get('/api/v1/department/'+$routeParams.departmentId+'/').success(function(data){
        $scope.department = data.data;
    });
    $scope.submit = function() {
        $http.delete('/api/v1/department/'+$routeParams.departmentId+'/', $scope.department).success(function(data) {
            $location.path('/departments').replace();
        }).error(function(){
            $scope.error;
        });
    };
});

angularControllers.controller('GroupList', function($scope, $http, $routeParams, $location, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
    });

    var dep_url_get = '';
    if($routeParams.departmentId){
        $scope.back_button = true;
        dep_url_get = '?department_id='+$routeParams.departmentId;
        $scope.setDepId($routeParams.departmentId);
    } else {
        $scope.setDepId(false);
    }

    $http.get('/api/v1/group/'+dep_url_get).success(function(data) {
        $scope.groups = data;
        $scope.show_group=false;
        if (data.status == "success"){
            $scope.show_group=true;
        }
        $scope.static = vars.static;
    });
    $scope.addButton = function(){
        if($scope.logged){
            $location.path('group/add').replace();
        } else {
            $scope.notLoggedMsg = true;
        }
    };
    $scope.editButton = function(dep_id){
        if($scope.logged){
            $location.path('group/edit/'+dep_id+'/').replace();
        } else {
            $scope.notLoggedMsg = true;
        }
    };
    $scope.deleteButton = function(dep_id){
        if($scope.logged){
            $location.path('group/delete/'+dep_id+'/').replace();
        } else {
            $scope.notLoggedMsg = true;
        }
    };
});

angularControllers.controller('GroupAdd', function($scope, $http, $location, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
    });

    if($scope.depId != false){
        $scope.backUrl = "departments/"+$scope.depId;
    } else {
        $scope.backUrl = "groups/";
    }

    $scope.group = '';

    $http.get('/api/v1/department/').success(function(data){
        $scope.departments = data.data;
        for(var i = 0; i < $scope.departments.length; i++){
            if($scope.departments[i].id == $scope.depId){
                $scope.department = $scope.departments[i];
                //$scope.department = $scope.departments[i];
                var dfdsafa = 0;
            }
        }
    });


    $scope.submit = function() {
        if ($scope.group.name) {
            var group = {
                "name": $scope.group.name,
                "department": $scope.department.id,
                "headman": ''
            };
            var date = $scope.student.birthday;
            var student = {
                fio: $scope.student.fio,
                birthday: date.getFullYear().toString()+'-'+(date.getMonth()+1).toString()+'-'+date.getDate().toString(),
                number_student_cart: $scope.student.number_student_cart
            };
            $http.post('/api/v1/group/', group)
            .success(function(data) {
                student.group = data.data.id;

                $http.post('/api/v1/student/', student).success(function(data){
                    group.headman = data.data.id;
                    $http.put('/api/v1/group/'+student.group+'/', group)
                    .success(function(data) {
                        if($scope.depId != false){
                            $location.path('departments/'+group.department).replace();
                        } else {
                            $location.path('groups/').replace();
                        }
                    });
                });
            });
        }
    };
});

angularControllers.controller('GroupEdit', function($scope, $http, $location, $routeParams, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
    });

    if($scope.depId != false){
        $scope.backUrl = "departments/"+$scope.depId;
    } else {
        $scope.backUrl = "groups/";
    }

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
        });
        $http.get('/api/v1/department/').success(function(data){
            $scope.departments = data.data;
            for(var i = 0; i < $scope.departments.length; i++){
                if($scope.departments[i].id == $scope.group.department){
                    $scope.group.department = $scope.departments[i];
                }
            }
        });
    });

    $scope.submit = function() {
        if ($scope.group.name) {
            if($scope.group.headman != null){
                $scope.group.headman = $scope.group.headman.id;
            } else {
                $scope.group.headman = '';
            }
            $scope.group.department = $scope.group.department.id;

            $http.put('/api/v1/group/'+$routeParams.groupId+'/', $scope.group)
            .success(function(data) {
                if($scope.depId != false){
                    $location.path('departments/'+$scope.group.department).replace();
                } else {
                    $location.path('groups/').replace();
                }
            });
        }
    };
});

angularControllers.controller('GroupDelete', function($scope, $http, $location, $routeParams, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
    });

    if($scope.depId != false){
        $scope.backUrl = "departments/"+$scope.depId;
    } else {
        $scope.backUrl = "groups/";
    }

    $http.get('/api/v1/group/'+ $routeParams.groupId +'/').success(function(data) {
        $scope.group = data.data;
    });

    $scope.submit = function() {
        $http.delete('/api/v1/group/'+$routeParams.groupId+'/', $scope.group).success(function(data) {
            if($scope.depId != false){
                $location.path('departments/'+$scope.group.department).replace();
            } else {
                $location.path('groups/').replace();
            }
        });

    };
});

angularControllers.controller('StudentList', function($scope, $http, $routeParams, $location, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
    });

    if($scope.depId != false){
        $scope.backUrl = "departments/"+$scope.depId;
    } else {
        $scope.backUrl = "groups/";
    }

    var dep_url_get = '';
    if($routeParams.groupId){
        $scope.back_button = true;
        dep_url_get = '?group_id='+$routeParams.groupId;
        $scope.setGroupId($routeParams.groupId);
    } else {
        $scope.setGroupId(false);
    }

    $http.get('/api/v1/student/'+dep_url_get)
        .success(function(data) {
            $scope.students = data;
            $scope.show_students=false;
            if (data.status == "success"){
                $scope.show_students=true;
            }
            $scope.static = vars.static;
            $scope.group_id = $routeParams.groupId
    });

    $scope.addButton = function(){
        if($scope.logged){
            $location.path('student/add').replace();
        } else {
            $scope.notLoggedMsg = true;
        }
    };
    $scope.editButton = function(dep_id){
        if($scope.logged){
            $location.path('student/edit/'+dep_id+'/').replace();
        } else {
            $scope.notLoggedMsg = true;
        }
    };
    $scope.deleteButton = function(dep_id){
        if($scope.logged){
            $location.path('student/delete/'+dep_id+'/').replace();
        } else {
            $scope.notLoggedMsg = true;
        }
    };
});

angularControllers.controller('StudentAdd', function($scope, $http, $location, $routeParams, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
    });

    if($scope.groupIdMain != false){
        $scope.backUrl = "groups/"+$scope.groupIdMain;
    } else {
        $scope.backUrl = "students/";
    }

    $http.get('/api/v1/group/').success(function(data){
        $scope.groups = data.data;
        for(var i = 0; i<$scope.groups.length; i++){
            if($scope.groups[i].id == $scope.groupIdMain){
                $scope.group = $scope.groups[i];
            }
        }
    });

    $scope.group_id = $routeParams.group_id;
    $scope.submit = function() {
        var date = $scope.student.birthday;
        var student = {
            fio: $scope.student.fio,
            birthday: date.getFullYear().toString()+'-'+(date.getMonth()+1).toString()+'-'+date.getDate().toString(),
            number_student_cart: $scope.student.number_student_cart,
            group: $scope.group.id
        };
        $http.post('/api/v1/student/', student).success(function(data){
            if($scope.groupIdMain != false){
                $location.path('/groups/'+student.group).replace();
            } else {
                $location.path('/students/').replace();
            }
        });
    };
});

angularControllers.controller('StudentEdit', function($scope, $http, $location, $routeParams, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
    });

    if($scope.groupIdMain != false){
        $scope.backUrl = "groups/"+$scope.groupIdMain;
    } else {
        $scope.backUrl = "students/";
    }

    $http.get('/api/v1/student/'+ $routeParams.studentId + '/').success(function(data) {
        $scope.student = data.data;
        $scope.student.birthday = new Date($scope.student.birthday);
        $http.get('/api/v1/group/').success(function(data) {
            $scope.groups = data.data;
            for(var i = 0; i<$scope.groups.length; i++){
                if($scope.groups[i].id == $scope.student.group){
                    $scope.student.group = $scope.groups[i];
                }
            }
        });
    });

    $scope.submit = function() {
        var date = $scope.student.birthday;
        var student = {
            fio: $scope.student.fio,
            birthday: date.getFullYear().toString()+'-'+(date.getMonth()+1).toString()+'-'+date.getDate().toString(),
            number_student_cart: $scope.student.number_student_cart,
            group: $scope.student.group.id
        };
        $http.put('/api/v1/student/'+$routeParams.studentId + '/', student)
        .success(function(data) {
            if($scope.groupIdMain != false){
                $location.path('/groups/'+$scope.student.group.id).replace();
            } else {
                $location.path('/students/').replace();
            }
        });
    };
});

angularControllers.controller('StudentDelete', function($scope, $http, $location, $routeParams, LoginService) {
    LoginService.isLogged().success(function(data){
        $scope.user = data.data.user;
        $scope.logged = true;
    }).error(function() {
        $scope.logged = false;
    });

    if($scope.groupIdMain != false){
        $scope.backUrl = "groups/"+$scope.groupIdMain;
    } else {
        $scope.backUrl = "students/";
    }

    $http.get('/api/v1/student/'+ $routeParams.studentId +'/').success(function(data) {
        $scope.student = data.data;
    });

    $scope.submit = function() {
        $http.delete('/api/v1/student/'+$routeParams.studentId+'/', $scope.student).success(function(data) {
            if($scope.groupIdMain != false){
                $location.path('/groups/'+$scope.student.group).replace();
            } else {
                $location.path('/students/').replace();
            }
        });

    };
});
