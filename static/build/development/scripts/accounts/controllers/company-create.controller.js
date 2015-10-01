(function () {
    'use strict';

    angular
        .module('accounts.controllers')
        .controller('CreateCompanyController', CreateCompanyController);

    CreateCompanyController.$inject = [
        '$scope', '$state', '$stateParams', 'Authentication', 'Account', 'Company','toastr',
    ];

    function CreateCompanyController($scope, $state, $stateParams, Authentication, Account, Company, toastr) {
        var vm = this;

        vm.company = {};

        activate();

        $scope.page = {
            title: 'Create Company',
        };

        function activate() {
            vm.authAcct = Authentication.getAuthenticatedAccount();
            console.log(vm.authAcct);
            if(vm.authAcct.optiz){
                Company.getOptiz()
                    .then(getOptizSuccess)
                    .catch(getOptizError);                
            }else{
                $state.go('app.dashboard');
            }

            function getOptizSuccess(data){
                console.log(data);
                vm.optizUsers = data;
            }

            function getOptizError(errorMsg){
                console.log(errorMsg);
            }
        }

        vm.createCompany = function(){
            console.log(vm.company);
            Company.create(vm.company)
                .then(createCompanySuccess)
                .catch(createCompanyError);
        }

        function createCompanySuccess(data){
            console.log(data);
            $state.go('app.pages.company-profile', {companyId:data.id}); 
        }

        function createCompanyError(errorMsg){
            toastr.error('There was a problem creating this company '+errorMsg+'');
        }

        vm.assignOptiz = function(optiz){
            console.log(optiz);
            var ao = {};
            ao['assign_optiz'] = optiz;
            Company.update(companyId, ao)
                .then(assignOptizSuccess)
                .catch(assignOptizError);
        }

        function assignOptizSuccess(data){
            console.log(data);
            vm.company = data;
            vm.addOptiz = data.company_assigned_to
            toastr.info('The account has been updated')
        }

        function assignOptizError(errorMsg){
            console.log(errorMsg);
        }

    };
})();