'use strict';

/**
 * @ngdoc function
 * @name spaceappApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the spaceappApp
 */
angular.module('spaceappApp')
    .controller('MainCtrl', function($scope, $http, NgMap) {
        NgMap.getMap().then(function(map) {
            $scope.map = map;
        });
        $http.get('http://eonet.sci.gsfc.nasa.gov/api/v2.1/events/EONET_358').then(function(response) {
            $scope.disaster = response.data;
        });

        $http.get('http://6848a814.ngrok.io/records/?country=philippines').then(function(response){
        	$scope.something = response.data.data;
        })

        $scope.googleMapsUrl = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyB5--PbJzFMC0_R-7ByRIwpDPcG7FofYRA';
        $scope.points = [
            { type: 'cough', position: [16.4023, 120.5960], place: 'Baguio', rating: 5 },
            { type: 'breath', position: [13.1162, 121.0794], place: 'Mindoro', rating: 4 },
            { type: 'sneeze', position: [10.3157, 123.8854], place: 'Cebu', rating: 4 },
            { type: 'itchy', position: [14.5995, 120.9842], place: 'Manila', rating: 8 }
        ];


        $scope.cough = {
            baguio: { population: 318676, position: [16.4023, 120.5960], rating: 5 }
        };
        $scope.itchy = {
            manila: { population: 10, position: [14.5995, 120.9842], rating: 4 }
        };

        $scope.sneeze = {
            cebu: { population: 120000, position: [10.3157, 123.8854], rating: 4 }
        };

        $scope.breath = {
            mindoro: { population: 120000, position: [13.1162, 121.0794], rating: 8 }
        };

        $scope.disasters = {
            position: [10.412, 123.132]
        };
        $scope.images = {
            url: 'http://maps.google.com/mapfiles/ms/micons/volcano.png'
        };

        $scope.showDetails = function(e,point,type) {
        	// $http.get('http://6848a814.ngrok.io/records/coordinates?lat='+point.latitude+'&lng='+point.longitude+'&distance=1').then(function(response){
        	// 	$scope.distances = response.data.data;
        	// 	console.log($scope.distances.distance);
        	// });
        	$scope.point = point;
        	$scope.location = point.raw_location;
        	if(type=='air'){
        		$scope.rating = point.air_pollution;
        	}else if(type=='cough'){
        		$scope.rating = point.caugh;
        	}else if(type=='breath'){
        		$scope.rating = point.shortness_of_breath;
        	}else if(type=='sneeze'){
        		$scope.rating = point.sneezing;
        	}
        	
        	$scope.map.showInfoWindow('points-iw',this);
        };

    }).filter('split', function() {
        return function(input, splitChar, splitIndex) {
            // do some bounds checking here to ensure it has that index
            return input.split(splitChar)[splitIndex];
        };
    });
