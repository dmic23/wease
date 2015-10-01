(function () {
  'use strict';

  angular
    .module('orders.controllers')
    .controller('OrderController', OrderController);

  OrderController.$inject = [
    '$scope', '$stateParams', '$state', '$log', 'Authentication', 'Account', 'Company', 'Order', 'Messages', 'toastr',
  ];

  function OrderController($scope, $stateParams, $state, $log, Authentication, Account, Company, Order, Messages, toastr) {
    var vm = this;

    activate();

    function activate() {
      vm.authenticatedAccount = Authentication.getAuthenticatedAccount();
      console.log(vm.authenticatedAccount);
      getOrder();
    }

    function getOrder(argument) {
      var orderId = $stateParams.orderId;
      Order.getOrder(orderId)
        .then(getOrderSuccess)
        .catch(getOrderError);
    }

    function getOrderSuccess(data) {
      vm.order = data;
      console.log(vm.order);
      var authUserCo = parseInt(vm.authenticatedAccount.user_company, 10);
      pageTitle(vm.order);
      if(vm.authenticatedAccount.optiz && vm.order.order_status === 'PEN'){
        toastr.info('Offer is needed for this order.');
      }
      if(authUserCo === vm.order.order_company.id){
        vm.orderCompany = true;
      }else{
        vm.orderCompany = false;
      }
      if(vm.order.order_offer){
        vm.curOfferTab = true;
        vm.auth_amount = false;
        console.log(vm.authenticatedAccount.auth_amount);
        var user_auth = parseInt(vm.authenticatedAccount.auth_amount, 10);
        console.log(user_auth);
        console.log(vm.order.order_total);
        var offer_total = parseInt(vm.order.order_total, 10);
        if(user_auth >= offer_total){
          vm.auth_amount = true;
        }else if(vm.authenticatedAccount.access_level >= 6){
          vm.auth_amount = true; 
        }
      }else{
        vm.reqTab = true;
      }

      getActivity();

    }

    function getOrderError(errorMsg) {
      $state.go('app.dashboard');
      toastr.error('Your request can not be processed '+errorMsg+' . Please contact Optiz');
    }

    function getActivity(){
      Messages.orderActivity(vm.order.id)
        .then(orderActivitySuccess)
        .catch(orderActivityError);
    }

    function orderActivitySuccess(data){
      console.log(data);
      vm.orderActivity = data;
    }

    function orderActivityError(errorMsg){
      console.log(errorMsg);
    }

    function pageTitle(ordInfo){
      if(ordInfo.order_offer === false){
        $scope.page={ title : 'Request'};
      } else if (['OFR','REF'].indexOf(ordInfo.order_status)!=-1){
        $scope.page={ title : 'Offer'};
      } else {
        $scope.page={ title : 'Order'};
      } 
    }

    vm.confirmReq = function(reqInfo){
      console.log(reqInfo);
      console.log(reqInfo.id);
      if(!reqInfo.delivery_address || reqInfo.delivery_address === 'Null'){
        toastr.error('Please add a Delivery Address');
      } else {
        console.log(reqInfo);
        console.log(reqInfo.id);
        var draft = {};
        draft.order_draft = 'False';
        Order.addToOrder(reqInfo.id, draft)
          .then(confirmReqSuccess)
          .catch(confirmReqError);
      }
    }

    function confirmReqSuccess(data, status, headers, config){
      console.log(data);
      vm.order = data;
      pageTitle(vm.order);
      if (vm.order.order_status === 'PEN') {
        toastr.success('Your Request has been submitted to Optiz');
      } else {
        toastr.success('Your Request has been submitted to '+vm.order.order_company.name+' management for approval.');
      }
      getActivity();
    }

    function confirmReqError(errorMsg) {
      toastr.error('Your request can not be processed '+errorMsg+'. Please contact Optiz.');
    }

    vm.reqApvl = function(reqApv){
      var reqStat = {};
      reqStat.order_status = reqApv;
      reqStat.company_approval_status = reqApv;
      Order.addToOrder(vm.order.id, reqApv)
        .then(updateReqStatusSuccess)
        .catch(updateReqStatusError);
    }

    function updateReqStatusSuccess(data){
      console.log(data);
      vm.order = data;
      getActivity();
    }

    function updateReqStatusError(errorMsg){
      toastr.error('Your request can not be processed '+errorMsg+' . Please contact Optiz');
    }

    vm.orderStat = function(stat){
      console.log(stat);
      var ordStat = {};
      ordStat.order_status = stat;
      ordStat.optiz_status = stat;
      console.log(ordStat);
      Order.addToOrder(vm.order.id, ordStat)
        .then(updateReqStatusSuccess)
        .catch(updateReqStatusError);
    }

    vm.offerApvl = function(status){
      console.log(status);
      var stat = {};
      stat.offer = vm.order.offer_order[vm.order.offer_order.length - 1].id;
      stat.order_status = status;
      stat.company_approval_status = status;
      console.log(stat);
      console.log(vm.order.id);
      Order.addToOrder(vm.order.id, stat)
        .then(updateOfferSuccess)
        .catch(updateOfferError);
    }

    function updateOfferSuccess(data, status, headers, config) {
      console.log(data);
      vm.order = data;
      pageTitle(vm.order);
      toastr.info('Your response has been sent to Optiz');
      getActivity();   
    }

    function updateOfferError(errorMsg) {
      toastr.error('Your request can not be processed '+errorMsg+' . Please contact Optiz');
    }

    vm.addRef = function(rn){
      var refNum = {};
      refNum.reference_number = rn;
      Order.addToOrder(vm.order.id, refNum)
        .then(addRefSuccess)
        .catch(addRefError);
    }

    function addRefSuccess(data, status, headers, config) {
      console.log(data);
      vm.order.reference_number = data.reference_number; 
    }

    function addRefError(errorMsg) {
      vm.order.reference_number = vm.order.reference_number;
      toastr.error('Your request can not be processed '+errorMsg+' . Please contact Optiz');
    }

    vm.addAddr = function(addr){
      console.log(addr);
      vm.order['delivery_address'] = addr;
      console.log(vm.order.delivery_address);
      var delAddr = {};
      delAddr.delivery_address = addr.id;
      Order.addToOrder(vm.order.id, delAddr)
        .then(addAddrSuccess)
        .catch(addAddrError);
    }

    function addAddrSuccess(data, status, headers, config) {
      console.log(data);
      vm.order.delivery_address = data.delivery_address; 
    }

    function addAddrError(errorMsg) {
      vm.order.delivery_address = vm.order.delivery_address;
      toastr.error('Your request can not be processed '+errorMsg+' . Please contact Optiz');
    }

    vm.delOrder = function(orderId) {
      Order.delOrder(orderId)
        .then(delOrderSuccess)
        .catch(delOrderError);
    }

    function delOrderSuccess(data, status, headers, config) {
      console.log(data);
      $state.go('app.dashboard');
      toastr.info('Your order has been deleted');
    }

    function delOrderError(errorMsg) {
      toastr.error('Your request can not be processed '+errorMsg+' . Please contact Optiz');
    }

    vm.delReqItem = function(reqId) {
      Order.delReqItem(reqId)
        .then(delReqItemSuccess)
        .catch(delReqItemError);
    }

    function delReqItemSuccess(data, status, headers, config) {
      console.log(data);
      console.log(status);
      getOrder();
      toastr.info('Your request Item has been removed');
    }

    function delReqItemError(errorMsg) {
      toastr.error('Your request can not be processed '+errorMsg+' . Please contact Optiz');
    }

  }
})();
