(function () {
    'use strict';

    angular
        .module('orders.controllers')
        .controller('CommentController', CommentController);

    CommentController.$inject = [
        '$scope', '$stateParams', '$log', 'Authentication', 'Order', 'toastr'
    ];

    function CommentController($scope, $stateParams, $log, Authentication,  Order, toastr) {
        var vm = this;

        var orderId = $stateParams.orderId;

        vm.ordComment = {};

        vm.addComment = function(){
            console.log(orderId);
            console.log(vm.ordComment);
            Order.addToOrder(orderId, vm.ordComment)
                .then(commentSuccess)
                .catch(commentError);
        }

        function commentSuccess(data) {
            console.log(data);
            console.log(data.order_comment);
            $scope.comments = data.order_comment;
            vm.clearComment(); 
        }

        function commentError(errorMsg) {
            toastr.error('There was an error adding your comment. Please contact Optiz.');
        }

        vm.clearComment = function(){
            vm.ordComment = {};
        }
    }
})();
