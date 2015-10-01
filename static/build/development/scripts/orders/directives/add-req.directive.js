(function () {
    'use strict';

    angular
        .module('orders.directives')
        .directive('addReq', addReq);

    function addReq($sce) {

        var directive = {
            controller: 'AddRequestController',
            controllerAs: 'vm',
            restrict: 'E',
            scope: {
                req: '=',
                comp: '=',
            },
            templateUrl: $sce.trustAsResourceUrl(static_path('views/directives/addreq-directive.html')),
        }

        return directive;
    }
})();