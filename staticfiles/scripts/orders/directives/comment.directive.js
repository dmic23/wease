(function () {
  'use strict';

  angular
    .module('orders.directives')
    .directive('comment', comment);

  function comment($sce) {

	var directive = {
		// transclude:true,
    controller: 'CommentController',
    controllerAs: 'vm',
		restrict: 'E',
    // replace: true,
		scope: {
      path: '=',
			user: '=',
      comments: '=',
		},
        templateUrl: $sce.trustAsResourceUrl(static_path('views/directives/comment-directive.html')),
	}
    return directive;
  }

})();