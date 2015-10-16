(function () {
  'use strict';

  angular
    .module('orders.services')
    .factory('Order', Order);

  Order.$inject = ['$http', '$q'];

  function Order($http, $q) {
  	var Order = {
          getAll: getAll,
          getAllSimple: getAllSimple,
          getAllApv: getAllApv,
          getOrder: getOrder,
          createOffer: createOffer,
          createBlankOffer: createBlankOffer,
          addToOrder: addToOrder,
          delOrder: delOrder,
          delReqItem: delReqItem,
    };

    return Order;

    function generalCallbackSuccess(response){
      return response.data;
    }

    function generalCallbackError(response){
      return $q.reject('Error retrieving order details '+response.status+'');
    }

    // Get all orders
    function getAll() {
      return $http.get('api/v1/orders/')
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

    // Get simple orders
    function getAllSimple() {
      return $http.get('api/v1/order-simple/')
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

    // Get orders need approval
    function getAllApv(){
      return $http.get('api/v1/order-apv/')
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    } 
       
    // Get single order details
    function getOrder(orderId) {
      return $http.get('api/v1/orders/'+orderId+'/')
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

    // Create a blank offer
    function createBlankOffer(data) {
      console.log(data);
      return $http.post('/api/v1/offers/', data)
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

    // Create order offer
    function createOffer(orderId, data) {
      console.log(orderId);
      console.log(data);
      return $http.post('/api/v1/orders/'+orderId+'/offers/', data)
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

    // Add or update order
    function addToOrder(orderId, data) {
      console.log(orderId);
      console.log(data);
      return $http.put('/api/v1/orders/'+orderId+'/', data)
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

    // Delete order
    function delOrder(orderId) {
      console.log(orderId);
      return $http.delete('/api/v1/orders/'+orderId+'/')
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

    //Remove Request Item
    function delReqItem(reqId) {
      console.log(reqId);
      return $http.delete('/api/v1/req-items/'+reqId+'/')
        .then(generalCallbackSuccess)
        .catch(generalCallbackError);
    }

  }
})();