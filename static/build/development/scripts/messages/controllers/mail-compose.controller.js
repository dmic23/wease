(function () {
    'use strict';

    angular
        .module('messages.controllers')
        .controller('MailComposeController', MailComposeController);

    MailComposeController.$inject = ['$scope', '$state', '$stateParams', '$cookies','Authentication', 'Account', 'Messages', 'Company', 'FileUploader', 'toastr',];

    function MailComposeController($scope, $state, $stateParams, $cookies, Authentication, Account, Messages, Company, FileUploader, toastr) {
        var vm = this;

        vm.msgId = $stateParams.filterParam;

        activate();

        vm.toUsers = [];

        vm.newMail = {};

        function activate(){
            vm.user = Authentication.getAuthenticatedAccount();
            console.log(vm.user);
            if(vm.user.optiz){
                Account.getAll()
                .then(getAllSuccess)
                .catch(getCompanyAndOptizError);
            }else{
                Company.get($scope.au.user_company)
                .then(getCompanySuccess)
                .catch(getCompanyAndOptizError);
                Company.getOptiz()
                .then(getOptizSuccess)
                .catch(getCompanyAndOptizError);
            }
            if(vm.msgId){
                getDraft(vm.msgId);
            }

            $scope.isCollapsed = true;
        }

        function getAllSuccess(data){
            console.log(data);
            vm.toUsers = data;
            console.log(vm.toUsers);
        }

        function getCompanySuccess(data){
            console.log(data);
            vm.userCompany = data.wease_company;
        }

        function getOptizSuccess(data){
            console.log(data);
            vm.optizUsers = data;
            setUsers();
        }

        function getCompanyAndOptizError(errorMsg){
            console.log(errorMsg);
        }

        function setUsers(){
            angular.forEach(vm.userCompany, function (compUser, key){
                vm.toUsers.push(compUser);
            });
            angular.forEach(vm.optizUsers, function (optizUser, key){
                vm.toUsers.push(optizUser);
            });
            console.log(vm.toUsers);
        }

        function getDraft(msgId){
            Messages.getSingleMessage(msgId)
                .then(getDraftSuccess)
                .catch(getDraftError);
        }

        function getDraftSuccess(data){
            console.log(data);
            vm.newMail = data;
            console.log(vm.newMail);
        }

        function getDraftError(errorMsg){
            console.log(errorMsg);
            toastr.error('There was an issue to retrieve your message. Please contact Optiz.');
        }

        vm.sendMail = function (newMail){
            console.log(newMail)
            var updMail = _.omit(vm.newMail, 'mail_to');
            console.log(updMail);
            updMail.mailTo = [];
            console.log(updMail);
            angular.forEach(newMail.mail_to, function(v,k,o){
                updMail.mailTo.push(v.id);
            })
            console.log(updMail);
            if(vm.newMail.id){
                Messages.updateMessage(newMail.id, updMail)
                    .then(newMessageSuccess)
                    .catch(newMessageError);
            }else{
                Messages.newMessage(updMail)
                    .then(newMessageSuccess)
                    .catch(newMessageError);
            }
        }

        function newMessageSuccess(data){
            console.log(data);
            vm.msgId = data.id
            console.log(vm.msgId);
            if(data.mail_draft === true){
                vm.newMail = data;
                console.log(vm.newMail);
                toastr.info('Message saved as Draft');
            }

            if (uploader.queue.length>0){
                uploader.uploadAll()
            }else{
               $state.go('app.mail.inbox');
            }
            vm.newMail = {};

        }

        function newMessageError(errorMsg){
            console.log(errorMsg);
        }

        vm.cancel = function(){
            vm.newMail = {};
            $state.go('app.mail.inbox');
        }

        var csrf_token = $cookies.csrftoken;
        var uploader = $scope.uploader = new FileUploader({
            method: 'POST',
            url: '/api/v1/mail/'+vm.msgId+'/mail-files/',
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
        };
        uploader.onAfterAddingAll = function(addedFileItems) {
            console.info('onAfterAddingAll', addedFileItems);
        };
        uploader.onBeforeUploadItem = function(item) {
            console.info('onBeforeUploadItem', item);
            item.url = '/api/v1/mail/'+vm.msgId+'/mail-file/';
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
        };
        uploader.onCompleteAll = function() {
            console.info('onCompleteAll');
            $state.go('app.mail.inbox');
        };

        console.info('uploader', uploader);        

    }
})();