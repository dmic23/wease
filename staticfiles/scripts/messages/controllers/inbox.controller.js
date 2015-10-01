(function () {
  'use strict';

  angular
    .module('messages.controllers')
    .controller('InboxController', InboxController);

  InboxController.$inject = ['$scope', '$state', '$stateParams', '$dragon', 'Messages'];

  function InboxController($scope, $state, $stateParams, $dragon, Messages) {
    var vm = this;

    vm.fp = $stateParams.filterParam;
    console.log(vm.fp);

    vm.messages = {};
    vm.mail = {};
	vm.mail['selected'] = false;

	vm.selectAll = function() {

		if (vm.selectedAll === true) {
			vm.mail['selected'] = true;
		} else {
			vm.mail['selected'] = false;
		}

		angular.forEach($scope.mails, function(mail) {
			mail.selected = $scope.selectedAll;
		});
	};


    Messages.getAllMail($scope.au)
        .then(getAllMessagesSuccess)
        .catch(getAllMessagesError);

    function getAllMessagesSuccess(response){
        console.log(response);
        if(vm.fp === 'sent'){
        	vm.messages = response.sent;
        }else if(vm.fp === 'draft'){
        	vm.messages = response.draft;
        }else if(vm.fp === 'trash'){
        	vm.messages = response.trash;
    	}else{
    		vm.messages = response.inbox;
    	}
        console.log(vm.messages);
    }

    function getAllMessagesError(errorMsg){
        console.log(errorMsg);
    }
    // console.log($scope.au);
    // console.log($scope.msgs)
    // vm.messages = $scope.msgs;
    $scope.$on("update_mail", function(event, message) {
        // $scope.msgs = message;
        console.log(message);
        if(vm.fp === 'sent'){
            vm.messages = message.sent;
        }else if(vm.fp === 'draft'){
            vm.messages = message.draft;
        }else if(vm.fp === 'trash'){
            vm.messages = message.trash;
        }else{
            vm.messages = message.inbox;
        }
        console.log(vm.messages);
    });
    // $scope.channel = 'mail';
    // $dragon.onReady(function() {
    //     $dragon.subscribe('mail', $scope.channel, {}).then(function(response) {
    //         $scope.dataMapper = new DataMapper(response.data);
    //         console.log($scope.dataMapper);
    //     });

    //     // $dragon.getList('mail', {}).then(function(response) {
    //     //     console.log(response.data);
    //     //     // getAllMessagesSuccess(response.data);
    //     // });
    //     // $dragon.getList('mail-reply', {}).then(function(response) {
    //     //     console.log(response.data);
    //     //     getAllMessagesSuccess(response.data);
    //     // });
    // });

    // $dragon.onChannelMessage(function(channels, message) {
    //     if (indexOf.call(channels, $scope.channel) > -1) {
    //         $scope.$apply(function() {
    //             // $scope.dataMapper.mapData(vm.messages, message);
    //             console.log('channel here');
    //             Messages.getAllMail($scope.au)
    //                 .then(getAllMessagesSuccess)
    //                 .catch(getAllMessagesError);

    //         });
    //     }
    // });

  }
})();