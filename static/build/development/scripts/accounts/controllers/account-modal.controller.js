'use strict';

angular.module('minovateApp')
  .controller('DeactivateUserModalCtrl', function ($scope, $modal, $log, $localStorage) {
    var vm = this;

    $scope.items = $localStorage.goods;

    $scope.open = function(size) {

      var modalInstance = $modal.open({
        templateUrl: static_path('views/modals/deactivate-user-modal.html'),
        controller: 'ModalInstanceCtrl',
        scope: $scope,
        size: size,
        resolve: {
          items: function () {
            return $scope.items;
          }
        }
      });

      modalInstance.result.then(function (selectedItem) {
        $scope.selected = selectedItem;
      }, function () {
        $log.info('Modal dismissed at: ' + new Date());
      });
    };
  })

  // Please note that $modalInstance represents a modal window (instance) dependency.
  // It is not the same as the $modal service used above.

  .controller('ModalInstanceCtrl', function ($scope, $modalInstance, items) {

    $scope.items = items;
    $scope.selected = {
      item: $scope.items[0]
    };

    $scope.ok = function () {
      $modalInstance.close($scope.selected.item);
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };
  });