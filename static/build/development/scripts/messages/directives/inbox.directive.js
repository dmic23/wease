(function () {
    'use strict';

    angular
        .module('messages.directives')
        .directive('inbox', inbox);

    function inbox($sce) {

        var directive = {
            restrict: 'E',
            scope: {
                path: '=',
                msgs: '=',
            },
            templateUrl: $sce.trustAsResourceUrl(static_path('views/directives/inbox.html')),
        }
        return directive;
    }
})();