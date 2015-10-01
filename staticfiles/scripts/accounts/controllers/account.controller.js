(function () {
    'use strict';

    angular
        .module('accounts.controllers')
        .controller('AccountController', AccountController);

    AccountController.$inject = [
        '$scope', '$state', '$stateParams', '$cookies', 'Authentication', 'Account', 'Company', 'FileUploader', 'toastr',
    ];

    function AccountController($scope, $state, $stateParams, $cookies, Authentication, Account, Company, FileUploader, toastr) {
        var vm = this;

        vm.destroy = destroy;
        vm.update = update;

        vm.username = $stateParams.username;

        activate();

        $scope.page = {
            title: 'Profile Page',
        };

        // activate function to initialize on page/controller load
        function activate() {
            // Get Auth user
            vm.authAcct = Authentication.getAuthenticatedAccount();
            console.log(vm.authAcct);
            // GET Account with success/error callbacks
            Account.get(vm.username)
                .then(accountSuccessFn)
                .catch(accountErrorFn);

            function accountSuccessFn(data) {
                vm.account = data;  
                console.log(vm.account); 
                getCompany();
                if(vm.authAcct.id === vm.account.id){
                    vm.isUser = true;
                }else{
                    vm.isUser = false;
                }
            }

            function accountErrorFn(errorMsg) {
                $state.go('app.dashboard');
                toastr.error('That user does not exist.');
            }
        }

        function getCompany(){
            console.log(vm.account.user_company);
            Company.get(vm.account.user_company)
              .then(companySuccessFn)
              .catch(companyErrorFn);  
        }

        // GET company details success/error callbacks
        function companySuccessFn(data, status, headers, config) {
            console.log(data);
            vm.company = data;
        }

        function companyErrorFn(data, status, headers, config) {
            console.log(data);
            $state.go('app.dashboard');
            toastr.error('That company does not exist.');
        }

        // Destroy Account with success/error callbacks
        function destroy() {
            Account.destroy(vm.account.username)
                .then(destroySuccessFn)
                .catch(destroyErrorFn);
        }

        function destroySuccessFn(data, status, headers, config) {
            Authentication.unauthenticate();
            $state.go('app.dashboard');
            toastr.warning('Your account has been deleted.');
        }

        function destroyErrorFn(errorMsg) {
            toastr.error(errorMsg);
        }

        // Update Account with success/error callbacks
        function update() {
            Account.update(vm.username, vm.account)
                .then(updateSuccessFn)
                .catch(updateErrorFn);
        }

        function updateSuccessFn(data, status, headers, config) {
            console.log(data);
            if(vm.account.id === vm.authAcct.id){
                vm.account = data;
                Authentication.setAuthenticatedAccount(data);
                $scope.$emit('update_user_info', data);
            }
            if(uploader.queue.length>0){
                uploader.uploadAll();
            }else{
                toastr.success('Your account has been updated.');
                getCompany();
            }
        }

        function updateErrorFn(data, status, headers, config) {
            toastr.error('There was an issue to update your account '+errorMsg+'. Please contact Optiz.');
        }

        var csrf_token = $cookies.csrftoken;
        var uploader = $scope.uploader = new FileUploader({
            method: 'PUT',
            url: '/api/v1/accounts/'+vm.username+'/',
            headers : {
                'X-CSRFToken': csrf_token 
            },
        });

        // FILTERS
        uploader.filters.push({
            name: 'customFilter',
            fn: function(item /*{File|FileLikeObject}*/, options) {
                return this.queue.length < 10;
            }
        });

        // CALLBACKS
        uploader.onWhenAddingFileFailed = function(item /*{File|FileLikeObject}*/, filter, options) {
            console.info('onWhenAddingFileFailed', item, filter, options);
        };
        uploader.onAfterAddingFile = function(fileItem) {
            console.info('onAfterAddingFile', fileItem);
            vm.isFile = true;
        };
        uploader.onAfterAddingAll = function(addedFileItems) {
            console.info('onAfterAddingAll', addedFileItems);
        };
        uploader.onBeforeUploadItem = function(item) {
            console.info('onBeforeUploadItem', item);
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
        };
        uploader.onCancelItem = function(fileItem, response, status, headers) {
            console.info('onCancelItem', fileItem, response, status, headers);
        };
        uploader.onCompleteItem = function(fileItem, response, status, headers) {
            console.info('onCompleteItem', fileItem, response, status, headers);
            vm.account.user_pic = response.user_pic; 
            getCompany();
            if(vm.account.id === vm.authAcct.id){
                Authentication.setAuthenticatedAccount(response);
                $scope.$emit('update_user_info', response);
            }
        };
        uploader.onCompleteAll = function() {
            console.info('onCompleteAll');
            toastr.success('Your account has been updated.');
        };

        console.info('uploader', uploader);        
    };
})();