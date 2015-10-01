(function () {
  'use strict';

  angular
    .module('orders.services')
    .factory('Offer', Offer);

  Offer.$inject = ['$http', '$q'];

  function Offer($http, $q) {

  	var Offer = {
      getDetails: getDetails,
      getReq: getReq,
  		createReq: createReq,
  		updateReq: updateReq,

    };
    return Offer;

    // Get Offer details
    function getOffer(goodId) {
      return $http.get('api/v1/goods/'+goodId+'/details/')
      .then(detailsResponse)
      .catch(detailsError);
    }

    function detailsResponse(response){
      console.log("Offer")
      console.log(response);
      console.log(response.data);
      return response.data;
    }

    function detailsError(response){
      return $q.reject('Error retrieving request details '+response.status+'');
    }
    
    function createOffer(orderId, data) {
      console.log(orderId);
      console.log(data);
      return $http.post('/api/v1/orders/'+orderId+'/offers/', data)
        .then(createOfferSuccess)
        .catch(createOfferError);
    }

    function createOfferSuccess(response){
      console.log(response.data);
      return response.data;
    }

    function createOfferError(response){
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