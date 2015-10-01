
(function () {
  'use strict';

  angular
    .module('layout.services')
    .factory('Goods', Goods);

  Goods.$inject = ['$http'];

  function Goods($http) {

    var Goods = {

      get: get,

    };

    return Goods;

    function get() {
      return $http.get('/api/v1/goods/')
        .then(getGoodSuccess)
        .catch(getGoodError);
    }

    function getGoodSuccess(response) {
      console.log(response);
      console.log(response.data);
      return response.data;
    }

    function getGoodError(response) {
      console.log(response);
      console.log(response.data);
      return response.status
    }

  }
})();