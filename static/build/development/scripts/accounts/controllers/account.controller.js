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

            function accountSuccessFn(data){
                vm.account = data;  
                console.log(vm.account); 
                getCompany();
                if(vm.authAcct.id === vm.account.id){
                    vm.isUser = true;
                }else{
                    vm.isUser = false;
                }
                if($scope.admin){
                    vm.isAdmin = true;
                    vm.confirm = {};
                }else{
                    vm.isAdmin = false;
                }
            }

            function accountErrorFn(errorMsg) {
                $state.go('app.dashboard');
                toastr.error('That user does not exist.');
            }
        }
        vm.access_level_val = {
            "Administrator": "8",
            "Manager": "7",
            "Approval": "6",
            "Submit": "5",
            "View": "2",
        }

        vm.access_level_full = {
            "8": "Administrator",
            "7": "Manager",
            "6": "Approval",
            "5": "Submit",
            "2": "View",
        }



        function getCompany(){
            console.log(vm.account.user_company);
            Company.get(vm.account.user_company)
              .then(companySuccessFn)
              .catch(companyErrorFn);  
        }

        // GET company details success/error callbacks
        function companySuccessFn(data) {
            console.log(data);
            vm.company = data;
        }

        function companyErrorFn(data) {
            console.log(data);
            $state.go('app.dashboard');
            toastr.error('That company does not exist.');
        }

        vm.deactivate = function(acct) {
            if(vm.isAdmin){
                acct['is_active'] = false;
                Account.update(acct)
                    .then(deactivateSuccess)
                    .catch(updateError);
            }
        }

        function deactivateSuccess(data) {
            //Authentication.unauthenticate();
            console.log(data);
            $state.go('app.dashboard');
            toastr.warning('Account has been deactivated.');
            if(vm.account.id === vm.authAcct.id){
                vm.account = data;
                Authentication.setAuthenticatedAccount(data);
                $scope.$emit('update_user_info', data);
            }
        }

        // Update Account with success/error callbacks
        vm.update = function(acct) {
            console.log(acct);
            Account.update(acct)
                .then(updateSuccess)
                .catch(updateError);
        }

        function updateSuccess(data) {
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

        function updateError(data) {
            toastr.error('There was an issue to update your account '+errorMsg+'. Please contact Optiz.');
        }

        var csrf_token = $cookies.csrftoken;
        var uploader = $scope.uploader = new FileUploader({
            method: 'PUT',
            url: '/api/v1/accounts/'+vm.username+'/',
            headers: {
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