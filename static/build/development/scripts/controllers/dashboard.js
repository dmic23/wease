'use strict';

/**
 * @ngdoc function
 * @name minovateApp.controller:DashboardCtrl
 * @description
 * # DashboardCtrl
 * Controller of the minovateApp
 */
angular.module('minovateApp')
  .controller('DashboardCtrl', function ($scope, $http){
    $scope.page = {
      title: 'Dashboard',
    };

  });

