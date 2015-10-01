(function () {
  'use strict';

  angular
    .module('orders.controllers')
    .controller('OrdersTableController', OrdersTableController);

  OrdersTableController.$inject = [
    '$scope', '$state', '$stateParams', '$log', 'Authentication', 'Account', 'Company', 'Order', 'toastr', 'DTOptionsBuilder', 'DTColumnDefBuilder', 'DTColumnBuilder'
  ];

  function OrdersTableController($scope, $state, $stateParams, $log, Authentication, Account, Company, Order, toastr, DTOptionsBuilder, DTColumnDefBuilder, DTColumnBuilder) {
    var vm = this;

    vm.authenticatedAccount = Authentication.getAuthenticatedAccount();
    
    vm.orders = [];

    vm.setFilter = setFilter;

    var fp = $stateParams.filterParam
    vm.filPar = {
      'WRQ': 'Demandes en attente',
      'PEN': 'Demandes à traiter',
      'OFR': 'Offre disponible',
      'APV': 'Approuvé',
      'REF': 'Refusé',
      'INP': 'In Progress',
      'COM': 'Completed',
      'INV': 'Invoiced',
      'CAN': 'Annulé',
      'ARC': 'Archived',
      'BOR': 'Backorder',
    }
    
    console.log(vm.filPar);
    console.log(fp);
    console.log(vm.filPar.fp);
    vm.filterInfo = vm.filPar[fp];

    Order.getAllSimple().then(getAllSuccess, getAllError);

    function getAllSuccess(data, status, headers, config) {
      vm.orders = data;
      console.log(vm.orders);
    }

    function getAllError(errorMsg) {
      $state.go('app.dashboard');
      toastr.error('Your request can not be processed '+errorMsg+'. Please contact Optiz.');
    }

    vm.dtOptions = DTOptionsBuilder.newOptions()
      .withBootstrap()
      .withOption('order', [[2, 'desc']])
      .withOption('search', { 'search': vm.filterInfo })
      .withDOM('<"row"<"col-md-8 col-sm-12"<"inline-controls"l>><"col-md-4 col-sm-12"<"pull-right"f>>>t<"row"<"col-md-4 col-sm-12"<"inline-controls"l>><"col-md-4 col-sm-12"<"inline-controls text-center"i>><"col-md-4 col-sm-12"p>>')
      .withLanguage({
        "sLengthMenu": 'View _MENU_ records',
        "sInfo":  'Found _TOTAL_ records',
        "oPaginate": {
          "sPage":    "Page",
          "sPageOf":  "of"
        }
      })
      .withPaginationType('input')
      // .withScroller()
      // .withOption("sScrollY", false)
      // .withOption("sScrollX")
      .withColumnFilter();


    vm.dtColumnDefs = [
      DTColumnDefBuilder.newColumnDef(9).notSortable(),
      DTColumnDefBuilder.newColumnDef(10).notVisible()
    ];

    vm.selectedAll = false;

    vm.selectAll = function () {

      if ($scope.selectedAll) {
        $scope.selectedAll = false;
      } else {
        $scope.selectedAll = true;
      }

      angular.forEach(vm.orders, function(order) {
        order.selected = $scope.selectedAll;
      });
    };

    function setFilter(fltr){
      console.log(fltr);
      vm.filterInfo = fltr;
      vm.dtOptions = DTOptionsBuilder.newOptions()
        .withBootstrap()
        .withOption('order', [[2, 'desc']])
        .withOption('search', { 'search': vm.filterInfo })
        .withDOM('<"row"<"col-md-8 col-sm-12"<"inline-controls"l>><"col-md-4 col-sm-12"<"pull-right"f>>>t<"row"<"col-md-4 col-sm-12"<"inline-controls"l>><"col-md-4 col-sm-12"<"inline-controls text-center"i>><"col-md-4 col-sm-12"p>>')
        .withLanguage({
          "sLengthMenu": 'View _MENU_ records',
          "sInfo":  'Found _TOTAL_ records',
          "oPaginate": {
            "sPage":    "Page",
            "sPageOf":  "of"
          }
        })
        .withPaginationType('input')
        .withColumnFilter();
    }
  }
})();
