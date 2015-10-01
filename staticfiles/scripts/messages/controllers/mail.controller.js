(function () {
  'use strict';

  angular
    .module('messages.controllers')
    .controller('MailController', MailController);

  MailController.$inject = ['$scope', '$state', '$stateParams', 'Authentication', 'Messages'];

  function MailController($scope, $state, $stateParams, Authentication, Messages) {
    var vm = this;

    activate();

    function activate(){
        vm.user = Authentication.getAuthenticatedAccount();
        console.log(vm.user);
    }
    
  }
})();
