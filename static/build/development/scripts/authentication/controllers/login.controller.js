
(function () {
  'use static';

  angular
    .module('authentication.controllers')
    .controller('LoginController', LoginController);

  LoginController.$inject = ['$scope', '$state', 'Authentication'];

  function LoginController($scope, $state, Authentication) {
    var vm = this;

    vm.login = login;

    activate();

    function activate() {

        // If the user is authenticated, they should not be here.
        if (Authentication.isAuthenticated()) {
          $state.go('app.dashboard');
        }
      }

      function login() {
        Authentication.login(vm.email, vm.password)
          .then(loginSuccess)
          .catch(loginError);
      }

      function loginSuccess(data){

      }

      function loginError(errorMsg){
        console.log(errorMsg);
        $scope.error = errorMsg;
      }
  }
})();
