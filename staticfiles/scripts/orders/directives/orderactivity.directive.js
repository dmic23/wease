(function () {
    'use strict';

    angular
        .module('orders.directives')
        .directive('orderActivity', orderActivity);

    orderActivity.$inject = ['$sce',];

    function orderActivity($sce) {

        var directive = {
            restrict: 'E',
            scope: {
                activity: '=',
                stati: '=',
            },          
            templateUrl: $sce.trustAsResourceUrl(static_path('views/directives/orderactivity-directive.html')),
        }

        return directive;
    }
})();