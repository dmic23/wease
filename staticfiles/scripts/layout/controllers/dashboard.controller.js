(function () {
    'use strict';

    angular
        .module('layout.controllers')
        .controller('DashboardController', DashboardController);

    DashboardController.$inject = ['$scope', '$filter', '$state', 'Authentication', 'Order', 'Messages'];

    function DashboardController($scope, $filter, $state, Authentication, Order, Messages) {
        var vm = this;

        vm.isAuthenticated = Authentication.isAuthenticated();
        console.log(vm.isAuthenticated);

        getOrderDetails();
        getLogs();

        $scope.page = {
            title: 'Dashboard',
        }
        
        vm.dashOrder = ['PEN', 'OFR', 'APV', 'INV'];

        function getOrderDetails(){
            Order.getAllSimple()
                .then(getOrderDetailsSuccess)
                .catch(getOrderDetailsError);
        }

        function getOrderDetailsSuccess(data){
            vm.orders = data;
            vm.icon = {
                'WRQ': 'fa-compass',
                'APN': 'fa-flag',
                'PEN': 'fa-ellipsis-v',
                'APV': 'fa-thumbs-o-up',
                'REF': 'fa-exclamation-triangle',
                'OFR': 'fa-pencil-square',
                'INP': 'fa-cogs',
                'COM': 'fa fa-check',
                'INV': 'fa-file-text', 
                'BOR': 'fa-asterisk',         
            }
            vm.verbiage = {
                'WRQ': 'Demandes en attente',
                'APN': 'Waiting Approval',
                'PEN': 'Demandes a traiter',
                'APV': 'Commandes validées',
                'REF': 'Offres refusées',
                'OFR': 'Offres disponibles',
                'INP': 'In Progress',
                'COM': 'Commandes finalisées',
                'INV': 'Facturées', 
                'BOR': 'Back Order',
            }
        }

        function getOrderDetailsError(errorMsg){
            console.log(errorMsg);
        }

        $scope.$on("update_dash", function(event, message) {
            vm.dashData = message;
        });

        function getLogs(){
            Messages.getNotifications()
                .then(getLogsSuccess)
                .catch(getLogsError);
        }

        function getLogsSuccess(data){
            console.log(data);
            vm.dashData = data;
        }

        function getLogsError(errorMsg){
            console.log(errorMsg);
        }

        vm.getDashInfo = function(dashItem){
            
            if(dashItem.not_action === 'comment added'){
                return 'A comment "'+dashItem.extra.comment+'" was added to #: '
            }else if(dashItem.not_action === 'request submitted'){
                return ' has submitted a new request # '
            }else if(dashItem.not_action === 'request created'){
                return ' has created a new request # '
            }else if(dashItem.not_action === 'request updated'){
                return ' has updated request # '
            }else if(dashItem.not_action === 'offer created'){
                return ' has submitted an offer # '
            }else if(dashItem.not_action === 'offer created'){
                return ' has submitted an offer # '
            }else if(dashItem.not_action === 'order status updated'){
                return ' has updated order # '
            }else if(dashItem.not_action === 'user created'){
                return ' has added a user '
            }else if(dashItem.not_action === 'company registered'){
                return ' has been registered with WeASe'
            }else if(dashItem.not_action === 'optiz assigned'){
                return ' has been assigned to '
            }else if(dashItem.not_action === 'company updated'){
                return ' has updated their profile information'
            }else{
                return 'Click to view!'
            }
        }

        vm.goToItem = function(dash){
            console.log(dash);
            if(dash.content_type === 'order'){
                $state.go('app.orders.order', {orderId:dash.object_id});
            }else{
                $state.go('app.pages.company-profile', {companyId:dash.object_id});
            }
        }
    }

})();



