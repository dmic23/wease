(function () {
    'use strict';

    angular
        .module('accounts.controllers')
        .controller('AddressController', AddressController);

    AddressController.$inject = [
        '$scope', '$stateParams', '$log', 'Authentication', 'Account', 'Company', 'toastr',
    ];

    function AddressController($scope, $stateParams, $log, Authentication, Account, Company, toastr) {
        var vm = this;

        // activate();

        function activate() {

        }

        vm.setAddr = function(addr, page){
            console.log(addr);
            console.log(page);
            if(page){
                console.log(addr);
                console.log(page);
            }else{
                console.log(addr);
                console.log(page);       
            }
        }

    }
})();
