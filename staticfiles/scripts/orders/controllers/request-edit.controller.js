(function () {
  'use strict';

  angular
    .module('orders.controllers')
    .controller('EditRequestController', EditRequestController);

  EditRequestController.$inject = [
    '$scope', '$location', '$state', '$stateParams', '$log', '$cookies', 'Authentication', 'Account', 'Company', 'Requests', 'FileUploader', 'toastr',
  ];

  function EditRequestController($scope, $location, $state, $stateParams, $log, $cookies, Authentication, Account, Company, Requests, FileUploader, toastr) {

    var vm = this;

    vm.reqId = $stateParams.reqId;

    activate();

    $scope.page = {
      title: 'Edit Request Item',
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

        Requests.getReq(vm.reqId).then(getReqSuccess).catch(getReqError);

        function getReqSuccess(data, status, headers, config) {
            vm.req = data;
            console.log("Req");
            console.log(vm.req);      
        }

        function getReqError(errorMsg) {
            $state.go('app.dashboard');
            // toastr.error('Your request can not be processed '+errorMsg+'');
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

    vm.updateReq = function (){
        console.log("Req Data");
        console.log(vm.req);
        console.log("good Deet");

        Requests.updateReq(vm.req)
            .then(updateReqSuccess)
            .catch(updateReqError);
    };

    function updateReqSuccess (data){
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

    function updateReqError (errorMsg){
        $log.error(errorMsg);

    }



    var csrf_token = $cookies.csrftoken;
    var uploader = $scope.uploader = new FileUploader({
      method: 'POST',
      url: '/api/v1/req-items/'+vm.reqId+'/req-files/',
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
      console.info('/api/v1/req-items/'+vm.reqId+'/req-files/');
      item.url = '/api/v1/req-items/'+vm.reqId+'/req-files/';
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
