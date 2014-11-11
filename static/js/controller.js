var StudentBaseApp = angular.module('AngularApp', ['ngRoute'])
    .controller('MainController', function($scope, $route, $routeParams, $location) {
     $scope.$route = $route;
     $scope.$location = $location;
     $scope.$routeParams = $routeParams;
 })

 .controller('BookController', function($scope, $routeParams) {
     $scope.name = "BookController";
     $scope.params = $routeParams;
 })

 .controller('ChapterController', function($scope, $routeParams) {
     $scope.name = "ChapterController";
     $scope.params = $routeParams;
 })

.config(function($routeProvider, $locationProvider) {
  $routeProvider
   .when('/Book/:bookId', {
    templateUrl: '/static/angular/book.html',
    controller: 'BookController',
    resolve: {
      // I will cause a 1 second delay
      delay: function($q, $timeout) {
        var delay = $q.defer();
        $timeout(delay.resolve, 1000);
        return delay.promise;
      }
    }
  })
  .when('/Book/:bookId/ch/:chapterId', {
    templateUrl: 'chapter.html',
    controller: 'ChapterController'
  });

  // configure html5 to get links working on jsfiddle
  $locationProvider.html5Mode(true);
});





















StudentBaseApp.config(function($interpolateProvider, $locationProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

StudentBaseApp.config(function($routeProvider, $locationProvider) {
    $routeProvider
        .when('/groups', {
            templateUrl: vars.static + 'group_list.html',

        });

    // configure html5 to get links working on jsfiddle
    $locationProvider.html5Mode(true);
});

StudentBaseApp.controller('GroupList', function($scope, $http, $location, $window) {
    $http.get('/api/v1/group/.json').success(function(data) {
        $scope.groups = data;
        $scope.show_group=false;
        if (data.status == "success"){
            $scope.show_group=true;
        }
        $scope.statics = vars.static;
        $scope.sss = vars.static + 'group_list.html';
    })
});

StudentBaseApp.controller('StudentList', function($scope, $http, $location, $window) {
    $http.get('/api/v1/group/.json').success(function(data) {
        $scope.groups = data;
        $scope.show_group=false;
        if (data.status == "success"){
            $scope.show_group=true;
        }
        $scope.statics = vars.static;
    })
    $scope.stt='studentsss';
});
