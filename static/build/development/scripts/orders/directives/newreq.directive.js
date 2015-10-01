(function () {
  'use strict';

  angular
    .module('orders.directives')
    .directive('newReq', newReq);

  function newReq($sce) {

	var directive = {
		// replace: true,
		// transclude:true,
    controller: 'RequestController',
    controllerAs: 'vm',
		restrict: 'E',
		scope: {
			req: '=',
      comp: '=',
		},
        templateUrl: $sce.trustAsResourceUrl(static_path('views/directives/newreq-directive.html')),
	}
    return directive;
  }

})();