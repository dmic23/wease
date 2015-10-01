(function () {
    'use strict';

    angular
        .module('messages.controllers')
        .controller('MailComposeController', MailComposeController);

    MailComposeController.$inject = ['$scope', '$state', '$stateParams', 'Authentication', 'Account', 'Messages', 'Company', 'toastr',];

    function MailComposeController($scope, $state, $stateParams, Authentication, Account, Messages, Company, toastr) {
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
            if(data.mail_draft === true){
                vm.newMail = data;
                console.log(vm.newMail);
                toastr.info('Message saved as Draft');
            }else{
                $state.go('app.mail.inbox');
            }
        }

        function newMessageError(errorMsg){
            console.log(errorMsg);
        }
    }
})();