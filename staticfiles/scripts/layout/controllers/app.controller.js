(function () {
    'use strict';

    angular
        .module('layout.controllers')
        .controller('AppController', AppController);

    AppController.$inject = ['$scope', '$cookies', '$dragon', 'Authentication', 'Order', 'Messages', 'toastr'];

    function AppController($scope, $cookies, $dragon, Authentication, Order, Messages, toastr) {
        var vm = this;

        vm.isAuthenticated = Authentication.isAuthenticated();
        console.log(vm.isAuthenticated);
        $scope.au = Authentication.getAuthenticatedAccount();

        $scope.$on("update_user_info", function(event, message){
            $scope.au = message;
        });
        console.log($scope.au);
        if($scope.au.access_level >= 8){
            $scope.admin = true;
            console.log($scope.admin);
        }
        if($scope.au.access_level >= 7){
            $scope.mgr = true;
            console.log($scope.mgr);
        }
        if($scope.au.access_level >= 6){
            $scope.apv = true;
            console.log($scope.apv);
        }
        if($scope.au.access_level >= 5){
            $scope.sub = true;
            console.log($scope.sub);
        }else{
            $scope.view = true;
            console.log($scope.view);
        }

        $scope.countries = ['France', 'Morocco', 'United States', 'Spain', 'Germany'];
        console.log($scope.countries);

        Order.getAllApv()
            .then(getAllApvSuccess)
            .catch(getAllApvError);

        function getAllApvSuccess(data){
            console.log(data);
            $scope.apvNeeded = [];
            angular.forEach(data, function(v, k, o) {
                $scope.apvNeeded.push(v.id);
            });
            console.log($scope.apvNeeded);
        }

        function getAllApvError(errorMsg){
            console.log(errorMsg);
        }

        Messages.getAllMail($scope.au)
            .then(getAllMailSuccess)
            .catch(getAllMailError);

        function getAllMailSuccess(data){
            console.log(data);
            $scope.msgs = data;
            $scope.$broadcast('update_mail', data);
        }

        function getAllMailError(errorMsg){
            console.log(errorMsg);
            toastr.error('There was an issue retreiving your messages...');
        }

        
        Messages.getNotifications()
            .then(getNotificationsSuccess)
            .catch(getNotificationsError);
    

        function getNotificationsSuccess(data){
            console.log(data);
            $scope.notifications = data;
            $scope.$broadcast('update_dash', data);
        }

        function getNotificationsError(errorMsg){
            console.log(errorMsg);
            vm.msgError = 'There was an issue with notifications';
        }

        $scope.mailChannel = 'mail';
        $scope.notChannel = 'notification';
        $dragon.onReady(function() {
            $dragon.subscribe('mail', $scope.mailChannel, {}).then(function(response) {
                // $scope.dataMapper = new DataMapper(response.data);
                // console.log($scope.dataMapper);
            });
            $dragon.subscribe('notification', $scope.notChannel, {}).then(function(response) {
                // $scope.dataMapper = new DataMapper(response.data);
                // console.log($scope.dataMapper);
            });
        });

        $dragon.onChannelMessage(function(channels, message) {
            if (indexOf.call(channels, $scope.mailChannel) > -1) {
                $scope.$apply(function() {
                    // $scope.dataMapper.mapData(vm.messages, message);
                    console.log('channel here');
                    Messages.getAllMail($scope.au)
                        .then(getAllMailSuccess)
                        .catch(getAllMailError);

                });
            }
            if (indexOf.call(channels, $scope.notChannel) > -1) {
                $scope.$apply(function() {
                    // $scope.dataMapper.mapData(vm.messages, message);
                    console.log('not channel here');
                    Messages.getNotifications()
                        .then(getNotificationsSuccess)
                        .catch(getNotificationsError);

                });
            }
        });



        $scope.stati = {
            'WRQ':'text-cyan',
            'PEN':'text-warning',
            'OFR':'text-drank',
            'APN':'text-dutch',
            'REF':'text-lightred',
            'APV':'text-greensea',
            'COM':'text-success',
            'CAN':'text-red',
            'ARC':'text-darkgray',
            'INP':'text-primary',
            'INV':'text-slategray',
        } 

        $scope.statiBg = {
            'WRQ':'bg-cyan',
            'PEN':'bg-warning',
            'OFR':'bg-drank',
            'APN':'bg-dutch',
            'REF':'bg-lightred',
            'APV':'bg-greensea',
            'COM':'bg-success',
            'CAN':'bg-red',
            'ARC':'bg-darkgray',
            'INP':'bg-primary',
            'INV':'bg-slategray',
        }

        $scope.notIcon = {
            'company registered': 'fa-university',
            'company updated': 'fa-plus',
            'user created': 'fa-user',
            'optiz assigned': 'fa-users',
            'request item created': 'fa-file-text-o',
            'request item updated': 'fa-pencil',
            'request submitted': 'fa-sign-in',
            'request created': 'fa-sign-out',
            'offer created': 'fa-clipboard', 
            'order status updated': 'fa-pencil-square-o',
            'comment added': 'fa-quote-right',          
        }

        $scope.notColor = {
            'company registered': 'bg-primary',
            'company updated': 'bg-slategray',
            'user created': 'bg-blue lt',
            'optiz assigned': 'bg-dutch',
            'request item created': 'bg-info',
            'request item updated': 'bg-amethyst dk',
            'request submitted': 'bg-hotpink dk',
            'request created': 'bg-greensea',
            'offer created': 'bg-drank',
            'order status updated': 'bg-default',
            'comment added': 'bg-slategray',
        }

        $scope.notTextColor = {
            'company registered': 'text-primary',
            'company updated': 'text-slategray',
            'user created': 'text-blue lt',
            'optiz assigned': 'text-dutch',
            'request item created': 'text-info',
            'request item updated': 'text-amethyst dk',
            'request submitted': 'text-hotpink dk',
            'request created': 'text-greensea',
            'offer created': 'text-drank',
            'order status updated': 'text-default',
            'comment added': 'text-slategray',
        }

    }
})();