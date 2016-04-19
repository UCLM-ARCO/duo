/* -*- mode: web; coding: utf-8 -*- */

var _ = console.info.bind(console);
var app = angular.module(
    'dummyBool', ['ngRoute'], function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
    }
);

app.controller("MainCtrl", function($scope, $location) {

    // FIXME: get these values from server
    $scope.state = get_property($location, "state", false) == "true";
    $scope.addr = get_property($location, "addr", "AA:10")

    $scope.on_show_qr = function() {
	if ($scope.qrcode != undefined) {
	    return;
	}

	$scope.qrcode = new QRCode("qrcode", {
	    text: $scope.addr,
	    width: 200,
	    height: 200,
	});
    };

    $scope.on_toggle_state = function() {
	$scope.state = ! $scope.state;
    };
});

function get_property($location, key, def_value) {
    var args = $location.search();
    if (args.hasOwnProperty(key))
	return args[key];
    return def_value;
}
