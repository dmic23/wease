
(function () {
  'use strict';

  angular
    .module('layout.controllers')
    .controller('NavController', NavController);

  NavController.$inject = ['$scope', '$state', '$localStorage', 'Authentication', 'Company', 'Goods'];

  function NavController($scope, $state, $localStorage, Authentication, Company, Goods) {  
    var vm = this;
    vm.icon = ['file-o','building','table','desktop','th-large','plus-square-o']
    vm.user = Authentication.getAuthenticatedAccount();
    console.log(vm.user);
    Goods.get().then(getGoodsSuccess).catch(getGoodsError);
    
    function getGoodsSuccess (goods){
      console.log(goods);
    	vm.allGoods = goods;
      $localStorage.goods = goods;
    	console.log(vm.allGoods);
    };

    function getGoodsError (msg){
    	console.log('Goods Error '+ msg);
    };

    if(vm.user.optiz){
      Company.getAll()
        .then(getAllSuccess)
        .catch(getAllError);
    }

    function getAllSuccess(data){
      console.log(data);
      vm.companies = data;
    }

    function getAllError(errorMsg){
      console.log(errorMsg);
    }

    // vm.goToCompany = function(companyId){
    //   console.log(companyId);
    //   var compId = companyId;
    //   $state.href('app.pages.company-profile', { comapnyId: compId });
    //   vm.comp = {};
    // }

    $scope.oneAtATime = false;

    $scope.status = {
      isFirstOpen: true,
      isSecondOpen: false,
      isThirdOpen: false
    };

  }
})();