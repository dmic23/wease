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
            unauthenticate: unauthenticate,
            deactivate: deactivate,
        };

        return Authentication;

        function generalCallbackSuccess(response){
            console.log(response.data);
            console.log(response);
            return response.data;
        }

        function generalCallbackError(response){
            console.log(response);
            console.log(response.data);
            return $q.reject('Error '+response.data.message+'');
        }

        function getAuthenticatedAccount() {
            console.log($cookies.authenticatedAccount);
            var authUserCookies = JSON.parse($cookies.authenticatedAccount);
            console.log(authUserCookies);
            if(authUserCookies.is_active){
                return authUserCookies;
            } else {
                logout();
            }
        }

        function isAuthenticated() {
            return !!$cookies.authenticatedAccount;
        }

        function login(email, password) {
            return $http.post('/api/v1/auth/login/', {
                email: email, 
                password: password
            }).then(loginSuccessFn).catch(generalCallbackError);
        }

        function loginSuccessFn(data) {
            Authentication.setAuthenticatedAccount(data.data);
            $state.go('app.dashboard');
        }

        function logout() {
            return $http.post('/api/v1/auth/logout/')
                .then(logoutSuccessFn)
                .catch(generalCallbackError);
        }

        function logoutSuccessFn(data) {
            Authentication.unauthenticate();
            $state.go('core.login');
        }

        function register(company, newUser) {
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
            })
            .then(generalCallbackSuccess).catch(registerError);
        }

        function registerError(response){
            if(_.has(response.data, 'username')){
                return $q.reject('Username must be unique');
            } 
            else if(_.has(response.data, 'email')){
                return $q.reject('Email must be unique');
            } else {
                return $q.reject('Error '+response.data.message+'');
            }
        }

        function setAuthenticatedAccount(acct) {
            $cookies.authenticatedAccount = JSON.stringify(acct);
        }

        function unauthenticate() {
            delete $cookies.authenticatedAccount;
        }

        function deactivate(acct){
            return $http.put('/api/v1/accounts/'+acct.id+'/', acct)
                .then(generalCallbackSuccess)
                .catch(generalCallbackError)
        }
  }
})();










