(function () {
  'use strict';

  angular
    .module('orders.controllers')
    .controller('RequestController', RequestController);

  RequestController.$inject = [
    '$scope', '$location', '$state', '$stateParams', '$log', '$cookies', 'Authentication', 'Account', 'Company', 'Requests', 'FileUploader', 'toastr',
  ];

  function RequestController($scope, $location, $state, $stateParams, $log, $cookies, Authentication, Account, Company, Requests, FileUploader, toastr) {

    var vm = this;
 
    var orderId = $stateParams.orderId;
    var reqId = $stateParams.reqId;
    var goodId = $stateParams.goodId;

    vm.newReq = {};
    vm.newReq.order_draft = true;
    // vm.updateReq = {};
    // $scope.oneAtATime = true;

    $scope.isCollapsed = true;

    $scope.status = {
      // isFirstOpen: true,
      // isFirstDisabled: false
    };
    // console.log(vm.newReq);
    // vm.destroy = destroy;
    // vm.update = update;

    // console.log($localStorage.aFile);
    // console.log($localStorage);

    // $scope.$watch(function () { return $localStorage.files; },function(newVal,oldVal){
    //     if(oldVal!==newVal && newVal === undefined){
    //         console.log($localStorage.files);
    //         console.log(oldVal);
    //         console.log(newVal); 
    //     }
    // });

    // $scope.$watch("vm.newReq", function(newValue, oldValue) {
    //     if($localStorage.aFile){
    //         if ($localStorage.aFile.length > 0) {
    //           // $scope.greeting = "Greetings " + $scope.name;
    //             console.log($localStorage.aFile);
    //             vm.store = []
    //             vm.store = {'req_file':$localStorage.aFile};
    //             console.log(vm.store);
    //             vm.newReq = vm.store;
    //         }
    //     }
    // });
    
    activate();

    $scope.page = {
      title: 'New Request Item',
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

    vm.isDraft = function (){
        if(vm.newReq.order_draft){
            vm.addReq();
        }
    };

    vm.addReq = function (){
        console.log("Req Data");
        console.log(vm.newReq);
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
        vm.newReq['good'] = vm.news;
        console.log(goodId);
        vm.newReq.good_id = goodId;
        console.log(vm.newReq.good_id);
        vm.newReq.add = false;
        console.log("Req Data 2");
        console.log(vm.newReq);

        Requests.createReq(vm.newReq)
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
        // $location.path('#/app/orders/order/'+data+'');
        // $state.go('app.orders.order', {orderId:data})
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
