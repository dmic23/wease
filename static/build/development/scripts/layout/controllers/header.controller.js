(function () {
    'use strict';

    angular
        .module('layout.controllers')
        .controller('HeaderController', HeaderController);

    HeaderController.$inject = ['$scope', '$state', 'Authentication', 'Messages',];

    function HeaderController($scope, $state, Authentication, Messages) { 
    
        var vm = this;
        vm.logout = logout;

        // getNotifications();

        function getNotifications(){
            Messages.getNotifications()
                .then(getNotificationsSuccess)
                .catch(getNotificationsError);
        }

        function getNotificationsSuccess(data){
            console.log(data);
            $scope.notifications = data;
        }

        function getNotificationsError(errorMsg){
            console.log(errorMsg);
            vm.msgError = 'There was an issue with notifications';
        }

        vm.goTo = function(notId){
            console.log(notId);
            Messages.notificationViewed(notId)
                .then(notificationViewedSuccess)
                .catch(notificationViewedError); 
        }

        function notificationViewedSuccess(data){
            console.log(data);
            getNotifications();
            if(data.content_type === 'order'){
                $state.go('app.orders.order', {orderId:data.object_id});
            }else{
                $state.go('app.pages.company-profile', {companyId:data.object_id});
            }
        }

        function notificationViewedError(errorMsg){
            console.log(errorMsg);
        }

        function logout() {
            Authentication.logout();
        }

    }
})();
