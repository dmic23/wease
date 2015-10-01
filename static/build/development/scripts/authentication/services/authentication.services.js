(function () {
    'use strict';

    angular
        .module('authentication.services')
        .factory('Authentication', Authentication);

    Authentication.$inject = ['$cookies', '$http', '$q', '$state', 'toastr'];

    function Authentication($cookies, $http, $q, $state, toastr) {

        var Authentication = {
            getAuthenticatedAccount: getAuthenticatedAccount,
            isAuthenticated: isAuthenticated,
            login: login,
            logout: logout,
            register: register,
            setAuthenticatedAccount: setAuthenticatedAccount,
            unauthenticate: unauthenticate
        };

        return Authentication;

        function getAuthenticatedAccount() {
            if (!$cookies.authenticatedAccount) {
                return;
            }
            return JSON.parse($cookies.authenticatedAccount);
        }

        function isAuthenticated() {
            console.log(!!$cookies.authenticatedAccount);
            return !!$cookies.authenticatedAccount;
        }

        function login(email, password) {
            return $http.post('/api/v1/auth/login/', {
                email: email, 
                password: password
            }).then(loginSuccessFn).catch(loginErrorFn);
        }

        function loginSuccessFn(data, status, headers, config) {
            Authentication.setAuthenticatedAccount(data.data);
            $state.go('app.dashboard');
        }

        function loginErrorFn(response) {
            console.log(response.data.message);
            console.log(response.status);
            return $q.reject(response.data.message);
        }

        function logout() {
            return $http.post('/api/v1/auth/logout/')
                .then(logoutSuccessFn)
                .catch(logoutErrorFn);
        }

        function logoutSuccessFn(data, status, headers, config) {
            Authentication.unauthenticate();
            $state.go('core.login');
        }

        function logoutErrorFn(response) {
            return $q.reject(response.status);
        }

        function register(company, newUser) {
            console.log(company);
            console.log(newUser);
            return $http.post('/api/v1/accounts/', {
                company: company, 
                username: newUser.username,
                email: newUser.email,
                position: newUser.position,
                access_level: newUser.access_level,
                auth_amount: newUser.auth_amount, 
                first_name: newUser.first_name,
                last_name: newUser.last_name,
                password: newUser.password,
                confirm_password: newUser.confirm_password
            }).then(registerSuccessFn).catch(registerErrorFn);
        }

        function registerSuccessFn(response) {
            return response.data;
        }

        function registerErrorFn(response) {
            console.log(response.data.message);
            console.log(response);
            return $q.reject(response.data.message);
        }

        function setAuthenticatedAccount(account) {
            $cookies.authenticatedAccount = JSON.stringify(account);
        }

        function unauthenticate() {
            delete $cookies.authenticatedAccount;
        }
  }
})();










