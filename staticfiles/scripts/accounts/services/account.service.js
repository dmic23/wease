(function () {
    'use strict';

    angular
        .module('accounts.services')
        .factory('Account', Account);

    Account.$inject = ['$http', '$q'];

    function Account($http, $q) {

        var Account = {
            destroy: destroy,
            getAll: getAll,
            get: get,
            update: update
        };

        return Account;

        function generalCallbackSuccess(response){
            console.log(response.data)
            console.log(response)
            return response.data;
        }

        function generalCallbackError(response){
            return $q.reject('Error '+response.status+'');
        }

        function destroy(username) {
            return $http.delete('/api/v1/accounts/' + username + '/')
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }

        function get(username) {
            return $http.get('/api/v1/accounts/' + username + '/')
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }

        function update(username, account) {
            return $http.put('/api/v1/accounts/' + username + '/', account)
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }    

        function getAll(){
            return $http.get('api/v1/accounts/')
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }

    }
})();
