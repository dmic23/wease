'use strict';

angular.module('minovateApp')
  .controller('MailInboxCtrl', function ($scope, $resource) {
    $scope.mails = $resource(static_path('scripts/jsons/mails.json')).query();

    $scope.selectedAll = false;

    $scope.selectAll = function () {

      if ($scope.selectedAll) {
        $scope.selectedAll = false;
      } else {
        $scope.selectedAll = true;
      }

      angular.forEach($scope.mails, function(mail) {
        mail.selected = $scope.selectedAll;
      });
    };
  });
