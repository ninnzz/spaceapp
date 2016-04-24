'use strict';

/**
 * @ngdoc function
 * @name spaceappApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the spaceappApp
 */
angular.module('spaceappApp')
  .controller('AboutCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
