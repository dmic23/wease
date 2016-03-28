(function () {
  'use strict';

  angular
    .module('authentication.controllers')
    .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$scope', 'Authentication'];

  function RegisterController($scope, Authentication) {
    var vm = this;

    vm.register = register;

    activate();

    function activate() {
      if (Authentication.isAuthenticated()) {

      }
    }

  }
})();
