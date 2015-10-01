(function () {
    'use strict';

    angular
        .module('orders.controllers')
        .controller('OfferController', OfferController);

    OfferController.$inject = [
        '$scope', '$filter', '$state', '$stateParams', '$log', '$cookies', 'Authentication', 'Account', 'Company', 'Order', 'Messages', 'toastr',
    ];

    function OfferController($scope, $filter, $state, $stateParams, $log, $cookies, Authentication, Account, Company, Order, Messages, toastr) {

        var vm = this;
     
        vm.orderId = $stateParams.orderId;

        vm.offer = {};
        vm.offer.offer_item = [];
        vm.offer.blank_item = [];

        activate();

        $scope.page = {
            title: 'Offer',
        };

        function activate() {
            var authenticatedAccount = Authentication.getAuthenticatedAccount();

            console.log(authenticatedAccount);
            if (!authenticatedAccount.optiz) {
                $state.go('core.login');
                toastr.error('You are not authorized to view this page.');
            } 
            getOrder();
        }
        console.log(vm.orderId);

        function getOrder(){
            Order.getOrder(vm.orderId)
                .then(getOrderSuccess)
                .catch(getOrderError);
        }

        function getOrderSuccess(data, status, headers, config) {
            vm.order = data;
            console.log(vm.order);
            if(vm.order.order_offer){
                $scope.page = {
                    ref_title: 'Offer',
                };
            }else{
                $scope.page = {
                    ref_title: 'Request',
                };
            }
            getActivity();
        }

        function getOrderError(errorMsg) {
            $state.go('app.dashboard');
            toastr.error('Your request can not be processed '+errorMsg+'');          
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

        console.log(vm.offer);

        vm.reqTab = true;

       vm.addItem = function(req_item){
          console.log(req_item);
          if(req_item.price){
            req_item.item_sub_total = req_item.quantity*req_item.price;
          }else{
            req_item.item_sub_total = 0;
          }
          console.log(req_item.item_name);
          console.log(vm.offer);
          // getTotal(req_item.item_sub_total);
          getTotal();
          toastr.success(req_item.item_name+' has been added to Current Offer');
          vm.reqTab = '';
          vm.offerTab = true;

        };

        vm.addBlankItem = function(blank_item){
            console.log(vm.offer.blank_item);
            console.log(blank_item);
            if(blank_item.price){
              blank_item.item_sub_total = blank_item.quantity*blank_item.price;
            }else{
              blank_item.item_sub_total = 0;
            }
            vm.offer.blank_item.push(blank_item);
            vm.blank_item = {};
            console.log(vm.offer);
            // getTotal(blank_item.item_sub_total);
            getTotal();
            toastr.success(blank_item.item_name+' has been added to Current Offer');
            vm.reqTab = '';
            vm.offerTab = true;
        }

        // function getTotal(item){
        //     console.log(vm.offer.blank_item);
        //     console.log(vm.offer.offer_item);
        //     console.log(item);
        //     if(vm.offer.offer_total){
        //         vm.offer['offer_total'] = vm.offer.offer_total += item;
        //     }else{
        //         vm.offer['offer_total'] = item;
        //     }
        //     if(!vm.offer.offer_total){
        //         vm.offer['offer_total'] = 0;
        //     }
        //     console.log(vm.offer.offer_total);
        //     console.log(vm.offer);
        // };

        function getTotal(){
            console.log(vm.offer.blank_item);
            console.log(vm.offer.offer_item);
            // console.log(item);
            // if(!vm.offer.offer_total){
            //     vm.offer['offer_total'] = 0;
            // }
            vm.offer['offer_total'] = 0;
            angular.forEach(vm.offer.offer_item, function(offItemValue, key, obj) {
              console.log(key);
              console.log(offItemValue);
              console.log(obj);
              angular.forEach(offItemValue, function(oiv, k, o) {
                if(k==='item_sub_total'){
                  console.log(k);
                  console.log(oiv);
                  console.log(o);
                  vm.offer['offer_total'] = vm.offer.offer_total += oiv;
                }
              })  
            })
            angular.forEach(vm.offer.blank_item, function(blankItemValue, key, obj) {
              console.log(key);
              console.log(blankItemValue);
              console.log(obj);
              angular.forEach(blankItemValue, function(biv, k, o) {
                if(k==='item_sub_total'){
                  console.log(k);
                  console.log(biv);
                  console.log(o);
                  vm.offer['offer_total'] = vm.offer.offer_total += biv;
                }
              })  
            })
            console.log(vm.offer.offer_total);
            console.log(vm.offer);
        };

        vm.addOffer = function (){
          console.log(vm.order);  
          console.log(vm.offer);
          if(!vm.offer.offer_terms){
            console.log(vm.offer);
            vm.offer['offer_terms'] = '';
            console.log(vm.offer.offer_terms);
          }
          console.log(vm.order.req_order[0].req_domain);
          vm.offer['offer_domain'] = vm.order.req_order[0].req_domain;
          vm.offer['order'] = vm.orderId
          angular.forEach(vm.offer.blank_item, function (value, prop, obj) {
              console.log(value); 
              console.log(prop); 
              console.log(obj);
              vm.offer.offer_item.push(value);
          });
          console.log(vm.offer);
          Order.createOffer(vm.orderId, vm.offer)
              .then(addOfferSuccess)
              .catch(addOfferError);
        };

        function addOfferSuccess(data){
            $log.info(data);
            $state.go('app.orders.order', {orderId:vm.orderId});  
        }

        function addOfferError(errorMsg){
            $log.error(errorMsg);
        }

        vm.delOfferItem = function(ofrItem){
          console.log(ofrItem);
          var index = vm.offer.offer_item.indexOf(ofrItem);
          vm.offer.offer_item.splice(index, 1); 
          getTotal();
        }

        vm.delBlankItem = function(ofrItem){
          console.log(ofrItem);
          var index = vm.offer.blank_item.indexOf(ofrItem);
          vm.offer.blank_item.splice(index, 1); 
          getTotal();
        }

        vm.cancelOffer = function(){
            console.log('cancel');
            vm.offer.offer_item = [];
            vm.offer.blank_item = [];            
            vm.offer = {};
            vm.order = {};
            $state.go('app.orders.order', {orderId:vm.orderId});
        };

    }

})();
