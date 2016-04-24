'use strict';

/**
 * @ngdoc function
 * @name spaceappApp.controller:DisasterlistCtrl
 * @description
 * # DisasterlistCtrl
 * Controller of the spaceappApp
 */
angular.module('spaceappApp')
    .controller('DisasterlistCtrl', function($scope, $http) {
        $http.get('http://eonet.sci.gsfc.nasa.gov/api/v2.1/events').then(function(response) {
            $scope.eventsList = response.data.events;
        });
        $scope.getLink = function(e) {
            console.log(e);
             $http.get(e).then(function(response) {
                 $scope.eventDetails = response.data;
                 console.log(response.data);
             });
        };
    }).filter('split', function() {
        return function(input, splitChar, splitIndex) {
            // do some bounds checking here to ensure it has that index
            return input.split(splitChar)[splitIndex];
        };
    });
