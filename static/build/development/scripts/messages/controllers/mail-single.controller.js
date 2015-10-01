(function () {
    'use strict';

    angular
        .module('messages.controllers')
        .controller('MailSingleController', MailSingleController);

    MailSingleController.$inject = ['$scope', '$state', '$stateParams', 'Authentication', 'Messages', 'toastr'];

    function MailSingleController($scope, $state, $stateParams, Authentication, Messages, toastr) {
        var vm = this;

        vm.mailReply = {};
        
        activate();

        function activate(){
            vm.user = Authentication.getAuthenticatedAccount();
            console.log(vm.user);
            vm.mailId = $stateParams.mailId;
            console.log(vm.mailId);
            Messages.getSingleMessage(vm.mailId)
                .then(getSingleMessageSuccess)
                .catch(getSingleMessageError);
        }

        function getSingleMessageSuccess(data){
            console.log(data);
            vm.mail = data;
        }

        function getSingleMessageError(errorMsg){
            console.log(errorMsg);
            toastr.error('There was an issue to retrieve your message. Please contact Optiz');
        }

        vm.sendReply = function(msg){
            vm.mailReply = _.pick(vm.mail, 'id', 'subject', 'mail_to', 'reply_to')
            vm.mailReply['mail_created_by'] = vm.mail.mail_created_by.id;
            vm.mailReply['body'] = msg;
            console.log(vm.mailReply)
            Messages.replyMessage(vm.mailId, vm.mailReply)
                .then(sendReplySuccess)
                .catch(sendReplyError);
        }

        function sendReplySuccess(data){
            console.log(data);
            $state.go('app.mail.inbox')
        }

        function sendReplyError(errorMsg){
            console.log(errorMsg);
        }

    }
})();
