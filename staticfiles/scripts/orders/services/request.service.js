(function () {
  'use strict';

  angular
    .module('orders.services')
    .factory('Requests', Requests);

  Requests.$inject = ['$http', '$q'];

  function Requests($http, $q) {

  	var Requests = {
      getDetails: getDetails,
      getReq: getReq,
  		createReq: createReq,
  		updateReq: updateReq,

    };
    return Requests;

    // Get request Item details
    function getDetails(goodId) {
      return $http.get('api/v1/goods/'+goodId+'/details/')
      .then(detailsResponse)
      .catch(detailsError);
    }

    function detailsResponse(response){
      console.log("good")
      console.log(response.data)
      return response.data;
    }

    function detailsError(response){
      return $q.reject('Error retrieving request details '+response.status+'');
    }

    // Get actual request item
    function getReq(reqId) {
      return $http.get('/api/v1/req-items/'+reqId+'/', {
      }).then(getReqSuccess)
        .catch(getReqError);
    }

    function getReqSuccess(response){
      return response.data;
    }

    function getReqError(response){
      return $q.reject('Error getting the request '+response.status+'');
      
    }
    
    // Create a new request item
    function createReq(data) {
      console.log(data);
      return $http.post('/api/v1/req-items/', data)
        .then(createReqSuccess)
        .catch(createReqError);
    }

    function createReqSuccess(response){
      console.log(response.data);
      return response.data;
    }

    function createReqError(response){
      return $q.reject('Error creating request '+response.status+'');
      
    }

    // Update request item
    function updateReq(reqInfo) {
      console.log(reqInfo);
      return $http.put('/api/v1/req-items/'+reqInfo.id+'/', {
        data: reqInfo
      }).then(updateReqSuccess)
        .catch(updateReqError);
    }

    function updateReqSuccess(response){
      console.log(response.data);
      return response.data;
    }

    function updateReqError(response){
      return $q.reject('Error updating the request '+response.status+''); 
    }


  }
})();