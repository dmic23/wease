(function () {
  'use strict';

  angular
    .module('orders.controllers')
    .controller('AddRequestController', AddRequestController);

  AddRequestController.$inject = [
    '$scope', '$state', '$stateParams', '$log', '$cookies', 'Authentication', 'Account', 'Company', 'Requests', 'Order','FileUploader', 'toastr',
  ];

  function AddRequestController($scope, $state, $stateParams, $log, $cookies, Authentication, Account, Company, Requests, Order, FileUploader, toastr) {

    var vm = this;
 
    vm.orderId = $stateParams.orderId;
    var goodId = $stateParams.goodId;
    console.log(goodId);
    vm.addReq = {};
    console.log(vm.addReq);

    // $scope.oneAtATime = true;

    $scope.isCollapsed = true;

    $scope.status = {
      // isFirstOpen: true,
      // isFirstDisabled: false
    };

    activate();

    $scope.page = {
      title: 'Add Request Item',
    };

    function activate() {
        var authenticatedAccount = Authentication.getAuthenticatedAccount();
        
        console.log(authenticatedAccount);
        if (!authenticatedAccount) {
            $state.go('core.login');
            toastr.error('You are not authorized to view this page.');
        } 
      // else {
      //   // Redirect if logged in, but not the owner of this account.
      //   if (authenticatedAccount) {
      //       // debugger;
      //       $location.url('/');
      //     // toastr.error('You are not authorized to view this page.');
      //     // console.log("2");
      //   }
      // }
        
        console.log(goodId);
        Requests.getDetails(goodId).then(detailsSuccess).catch(detailsError);

        function detailsSuccess(data, status, headers, config) {
            vm.details = data;
            console.log("Details");
            console.log(vm.details);
            for(var item in vm.details){
                console.log(vm.details[item].good);
            }
            console.log(vm.details[item].good);
            var par = vm.details[item].good.replace(/domain: | family: | subfamily: |' '/g,'');
            console.log(par);
            vm.news = par.split(',');
            console.log(vm.news);
        }

        function detailsError(errorMsg) {
            $state.go('app.dashboard');
            toastr.error('Your request can not be processed '+errorMsg+'');
        }

        Order.getOrder(vm.orderId).then(getOrderSuccess).catch(getOrderError);

        function getOrderSuccess(data, status, headers, config) {
          vm.order = data;
          console.log(vm.order);
          vm.addReq.order_id = vm.order.id;
          vm.addReq.order_draft = vm.order.order_draft;
          console.log(vm.order);
          console.log(vm.addReq);
        }

        function getOrderError(errorMsg) {
            $state.go('app.dashboard');
            toastr.error('Your request can not be processed '+errorMsg+'');          
        }

        Company.get(authenticatedAccount.user_company).then(companySuccess).catch(companyError);
        
        function companySuccess(data, status, headers, config) {
            vm.company = data;
            console.log("company");
            console.log(vm.company);      
        }

        function companyError(errorMsg) {
            $state.go('app.dashboard');
            toastr.error('Your request can not be processed '+errorMsg+'');
        }
    }

    vm.isDraft = function (){
        console.log("here");
        if(vm.addReq.order_draft){
            vm.addReq();
        }
    };

    vm.subReq = function (){
        console.log("Req Data");
        console.log(vm.addReq);
        console.log("good Deet");
        console.log(vm.details);
        // for(var item in vm.details){
        //     console.log(vm.details[item].good);
        // }
        // console.log(vm.details[item].good);
        // var par = vm.details[item].good.replace(/domain: | family: | subfamily: |' '/g,'');
        // console.log(par);
        // var news = par.split(',');
        console.log(vm.news);
        vm.addReq['good'] = vm.news;
        console.log(goodId);
        vm.addReq.good_id = goodId;
        console.log(vm.addReq.good_id);
        vm.addReq.add = true;
        console.log("Req Data 2");
        console.log(vm.addReq);
        Requests.createReq(vm.addReq)
            .then(addReqSuccess)
            .catch(addReqError);
    };

    function addReqSuccess (data){
        $log.info(data);
        $log.info(data.order);
        $log.info(data.id);
        vm.orderId = data.order;
        $log.info(vm.orderId);
        $scope.reqId = data.id;
        $log.info($scope.reqId);
        console.log(uploader)
        if (uploader.queue.length>0){
            uploader.uploadAll()
        }else{
           $state.go('app.orders.order', {orderId:vm.orderId}) 
        }
    }

        function addReqError (errorMsg){
            $log.error(errorMsg);

        }

        var csrf_token = $cookies.csrftoken;
        var uploader = $scope.uploader = new FileUploader({
          method: 'POST',
          url: '/api/v1/req-items/'+$scope.reqId+'/req-files/',
          headers : {
            'X-CSRFToken': csrf_token 
          },
         
        });

        // FILTERS
        uploader.filters.push({
          name: 'customFilter',
          fn: function() {
            return this.queue.length < 10;
          }
        });

        // CALLBACKS
        uploader.onWhenAddingFileFailed = function(item /*{File|FileLikeObject}*/, filter, options) {
            console.info('onWhenAddingFileFailed', item, filter, options);
        };
        uploader.onAfterAddingFile = function(fileItem) {
            console.info('onAfterAddingFile', fileItem);
        };
        uploader.onAfterAddingAll = function(addedFileItems) {
          console.info('onAfterAddingAll', addedFileItems);
        };
        uploader.onBeforeUploadItem = function(item) {
          console.info('onBeforeUploadItem', item);
          console.info(item.url);
          console.info('/api/v1/req-items/'+$scope.reqId+'/req-files/');
          item.url = '/api/v1/req-items/'+$scope.reqId+'/req-files/';
          console.info(item);
          return item         
        };
        uploader.onProgressItem = function(fileItem, progress) {
          console.info('onProgressItem', fileItem, progress);
        };
        uploader.onProgressAll = function(progress) {
          console.info('onProgressAll', progress);
        };
        uploader.onSuccessItem = function(fileItem, response, status, headers) {
          console.info('onSuccessItem', fileItem, response, status, headers);
        };
        uploader.onErrorItem = function(fileItem, response, status, headers) {
          console.info('onErrorItem', fileItem, response, status, headers);
          $state.go('app.orders.order', {orderId:vm.orderId})
        };
        uploader.onCancelItem = function(fileItem, response, status, headers) {
          console.info('onCancelItem', fileItem, response, status, headers);
          $state.go('app.orders.order', {orderId:vm.orderId})
        };
        uploader.onCompleteItem = function(fileItem, response, status, headers) {
          console.info('onCompleteItem', fileItem, response, status, headers);
        };
        uploader.onCompleteAll = function() {
          console.info('onCompleteAll');
          $state.go('app.orders.order', {orderId:vm.orderId})
        };

        console.info('uploader', uploader);
    }

})();
