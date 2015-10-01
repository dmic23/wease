(function () {
    'use strict';

    angular
        .module('orders.controllers')
        .controller('BlankOfferController', BlankOfferController);

    BlankOfferController.$inject = [
        '$scope', '$filter', '$state', '$stateParams', '$log', 'Goods', 'Authentication', 'Account', 'Company', 'Order', 'toastr',
    ];

    function BlankOfferController($scope, $filter, $state, $stateParams, $log, Goods, Authentication, Account, Company, Order, toastr) {

        var vm = this;
        // vm.offer = {};
        // vm.order = {};
        // vm.da = {};
        // vm.offer.offer_item = [];
        // vm.offer.blank_item = [];

        activate();

        $scope.page = {
            title: 'Blank Offer',
        };

        function activate() {
            var authenticatedAccount = Authentication.getAuthenticatedAccount();

            console.log(authenticatedAccount);
            if (!authenticatedAccount.optiz) {
                $state.go('app.dashboard');
            } 
            Company.getAll()
              .then(allCompanySuccess)
              .catch(allCompanyError);

            function allCompanySuccess(data){
              console.log(data);
              vm.companies = data;
            }

            function allCompanyError(errorMsg){
              console.log(errorMsg);
            }

            Goods.get().then(getGoodsSuccess).catch(getGoodsError);
    
            function getGoodsSuccess(goods){
                console.log(goods);
                vm.allGoods = goods;
                console.log(vm.allGoods);
                // vm.domains = [];
                // angular.forEach(goods, function(val, key, obj) {
                //     console.log(val.domain);
                //     console.log(key);
                //     console.log(obj);
                //     var dom = val.domain.toString();
                //     // if(!vm.domains.indexOf(val.domain)!=-1){
                //     //     console.log(val.domain);
                //     //     vm.domains.push(val.domain);
                //     // };
                //     if(_.contains(vm.domains, dom)!=-1){
                //         console.log(vm.domains);
                //         console.log(dom);
                //         vm.domains.push(dom);
                //     };
                //     console.log(vm.domains);
                // })
                // console.log(vm.domains);
            };

            function getGoodsError(msg){
                console.log('Goods Error '+ msg);
            };          
        };

        vm.selectComp = function(company) {
            console.log(vm.companies);
            console.log(company);
            vm.offer = {};
            vm.order = {};
            vm.da = {};
            vm.offer.offer_item = [];
            vm.offer.blank_item = [];
            vm.order.order_company = company;
            console.log(vm.order.order_company);
        };

        vm.addAddr = function(addr){
            console.log(addr);
            console.log(addr.id);
            vm.order['delivery_address'] = addr;
            vm.offer['delivery_address'] = addr.id;
            console.log(vm.order);
            console.log(vm.offer);
        };

        vm.addRef = function(refNum){
            console.log(refNum);
            vm.order['reference_number'] = refNum;
            vm.offer['reference_number'] = refNum;
            console.log(vm.order);
            console.log(vm.offer);
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
            getTotal(blank_item.item_sub_total);
            toastr.success(blank_item.item_name+' has been added to Current Offer');
            vm.offerTab = true;
        };

        function getTotal(){
            console.log(vm.offer.blank_item);
            vm.offer['offer_total'] = 0;
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
            console.log(vm.order.order_company);
            console.log(vm.offer);
            if(!vm.offer.delivery_address || vm.offer.delivery_address === 'Null'){
                toastr.error('Please add a delivery address');
            }else if(!vm.offer_domain){
                toastr.error('Please add a domain');
            }else{
                if(!vm.offer.offer_terms){
                    console.log(vm.offer);
                    vm.offer['offer_terms'] = '';
                    console.log(vm.offer.offer_terms);
                }
                console.log(vm.offer.blank_item);
                vm.offer['offer_domain'] = vm.offer_domain;
                vm.offer['offer_item'] = vm.offer.blank_item;
                vm.offer['blank_item'] = {};
                vm.offer['offer_company'] = vm.order.order_company.id;
                vm.offer['blank_offer'] = true;
                console.log(vm.offer);
                Order.createBlankOffer(vm.offer)
                    .then(addOfferSuccess)
                    .catch(addOfferError);
            }
        };

        function addOfferSuccess(data){
            $log.info(data);
            $state.go('app.orders.order', {orderId:data.order})  
        }

        function addOfferError(errorMsg){
            $log.error(errorMsg);
        }

        vm.delBlankItem = function(ofrItem){
            console.log(ofrItem);
            var index = vm.offer.blank_item.indexOf(ofrItem);
            vm.offer.blank_item.splice(index, 1);
            getTotal();
        };

        vm.cancelOffer = function(){
            console.log('cancel');
            vm.offer.offer_item = [];
            vm.offer.blank_item = [];            
            vm.offer = {};
            vm.order = {};
            vm.da = {};
            vm.comp = {};
        };

    }

})();
