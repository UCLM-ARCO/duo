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
    $scope.address = "AA:10";
    $scope.show_qr = false;

    $scope.$watch('address', on_address_change);
    sync_from_server($scope)

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
	    $scope.$apply();
	},
    });
}
