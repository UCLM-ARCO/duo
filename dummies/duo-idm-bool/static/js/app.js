/* -*- mode: web; coding: utf-8 -*- */

var _ = console.info.bind(console);
var app = angular.module(
    'dummyBool', ['ngRoute', 'ngAnimate'], function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
    }
);

app.controller("MainCtrl", function($scope) {
    $scope.state = false;
    $scope.icon = "lightbulb-o";
    $scope.address = "AA:10";
    $scope.observer = " - ";
    $scope.show_qr = false;

    $scope.$watch('address', on_address_change);
    sync_from_server($scope)
    new EventSource("/updates").onmessage = function(event) {
	on_incomming_update($scope, JSON.parse(event.data));
    }

    $scope.on_toggle_state = function() {
	$scope.state = ! $scope.state;
	$.ajax({ url: "/set", data: {state: $scope.state} });
    };
});

function on_address_change(newValue, oldValue) {
    var holder = "qrcode";
    $('#' + holder).children().remove();
    new QRCode(holder, {
	text: newValue,
	width: 200,
	height: 200,
    });
}

function sync_from_server($scope) {
    $.ajax({
	url: "/status",
	success: function(retval) {
	    var data = JSON.parse(retval);
	    $scope.state = data.state;
	    $scope.address = data.address;
	    $scope.icon = data.icon;
	    $scope.observer = data.observer || " - ";
	    $scope.$apply();
	},
    });
}

function on_incomming_update($scope, args) {
    $scope.state = args.state;
    $scope.$apply();
}
