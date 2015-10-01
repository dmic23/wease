(function () {
    'use strict';

    angular
        .module('accounts.directives')
        .directive('address', address);

    function address($sce) {

        var directive = {
            // transclude:true,
            controller: 'AddressController',
            controllerAs: 'vm',
            restrict: 'E',
            // replace: true,
            scope: {
                // path: '=',
                user: '=',
                addresses: '=',
                page: '=',
            },
            templateUrl: $sce.trustAsResourceUrl(static_path('views/directives/addr-directive.html')),
        }
        return directive;
    }
})();