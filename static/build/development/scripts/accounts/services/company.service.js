
(function () {
  'use strict';

  angular
    .module('accounts.services')
    .factory('Company', Company);

  Company.$inject = ['$http', '$q'];

  function Company($http, $q) {

    var Company = {
      getOptiz: getOptiz,
      getAll: getAll,
      get: get,
      create:create,
      destroy: destroy,
      update: update,
      newAddress: newAddress,
      updAddress: updAddress,
      destroyAddress: destroyAddress,
    };

    return Company;

    function generalCallbackSuccess(response){
      console.log(response.data)
      console.log(response)
      return response.data;
    }

    function generalCallbackError(response){
      return $q.reject('Error '+response.status+'');
    }

    function getOptiz(){
      return $http.get('api/v1/optiz')
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

    function getAll() {
      return $http.get('/api/v1/companies/')
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

    function get(companyId) {
      return $http.get('/api/v1/companies/' + companyId + '/')
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }
    
    function create(company) {
      console.log(company);
      return $http.post('/api/v1/companies/', company)
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

    function destroy(companyId) {
      return $http.delete('/api/v1/companies/' + companyId + '/')
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

    function update(companyId, company) {
      return $http.put('/api/v1/companies/' + companyId + '/', company)
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }      

    function newAddress(addr) {
      return $http.post('/api/v1/addresses/', addr)
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    } 

    function updAddress(addr) {
      return $http.put('/api/v1/addresses/'+addr.id+'/', addr)
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    } 

    function destroyAddress(addr){
      return $http.delete('api/v1/addresses/'+addr+'/')
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

  }
})();