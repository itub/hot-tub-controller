'use strict';

/* App Module */

var itubApp = angular.module('itubApp', [])
    .controller('itubController', ['$scope', '$http', function($scope, $http) {
        $scope.loaded = false;

        $http.get('/current').then(function(response) {
            $scope.loaded = true;
            var status = response.data;
            $scope.heater = status.heater;
            $scope.pump1 = status.pump1;
            $scope.pump2 = status.pump2;
            $scope.tempAir = ((status.tempAir * 9.0) / 5.0) + 32;
            $scope.tempIn = ((status.tempIn * 9.0) / 5.0) + 32;
            $scope.tempOut = ((status.tempOut * 9.0) / 5.0) + 32;
            $scope.tempSet = ((status.tempSet * 9.0) / 5.0) + 32;
        }).catch(function (err) {
            alert("Error retrieving status. " + err.statusText);
        });

        $scope.onchangeHeater = function() {
            var url = "/heater_";
            url += ($scope.heater == 0) ? "off" : "on";
            $http.get(url).then(function(response) {
                console.log("Heat control changed");
            }).catch(function (err) {
                alert("Error updating heat control");
            });
        };

        $scope.onchangePump1 = function() {
            var url = "/pump1_";
            if ($scope.pump1 === 0) {
                url += "off";
            } else if ($scope.pump1 === 1) {
                url += "low";
            } else if ($scope.pump1 === 2) {
                url += "high";
            } else {
                alert("Unexpected pump1 value");
                return;
            }
            $http.get(url).then(function(response) {
                console.log("pump1 changed");
            }).catch(function (err) {
                alert("Error updating pump1");
            });
        };

        $scope.onchangePump2 = function() {
            var url = "/pump2_";
            if ($scope.pump2 === 0) {
                url += "off";
            } else if ($scope.pump2 === 1) {
                url += "on";
            } else {
                alert("Unexpected pump2 value");
                return;
            }
            $http.get(url).then(function(response) {
                console.log("pump2 changed");
            }).catch(function (err) {
                alert("Error updating pump2");
            });
        };

    }]);
