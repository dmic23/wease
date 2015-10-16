(function () {
  'use strict';

  angular
    .module('messages.controllers')
    .controller('ChatController', ChatController);

  ChatController.$inject = ['$scope', '$dragon', 'Account', 'Company', 'Messages'];

  function ChatController($scope, $dragon, Account, Company, Messages) {
    var vm = this;

    activate();

    vm.toUsers = [];

    vm.chat = {};

    $scope.something = 'blah';

    function activate(){
        vm.user = $scope.au;
        console.log(vm.user);
        getChats();
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

    function getChats(){
        Messages.getChats()
            .then(getChatsSuccess)
            .catch(getChatsError);
    }

    function getChatsSuccess(response){
        console.log(response);
        vm.chats = response;
    }

    function getChatsError(errorMsg){
        console.log(errorMsg)
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

    vm.sendChat = function(chat, convo_id){
        console.log(chat);
        console.log(convo_id);
        if(!convo_id){

            var updChat = _.omit(chat, 'users');
            console.log('updcht', updChat);
            updChat.users = [];
            console.log(updChat);
            angular.forEach(chat.users, function(v,k){
                updChat.users.push(v.id);
                console.log(v.id);
                console.log(updChat)
            })
            updChat.users.push($scope.au.id);
            console.log(vm.chats);
            angular.forEach(vm.chats, function(cnv,k){
                console.log('dup users 1', cnv.chat_user);
                console.log('dup chat 1', updChat.users);
                if(cnv.chat_user.sort().join(',') === updChat.users.sort().join(',')){
                    vm.match = true;
                    console.log("---> MATCH <---");
                    console.log('dup users 2', cnv.chat_user.sort());
                    console.log(cnv);
                    console.log('dup chat 2', updChat.users.sort());
                    updChat['chatid'] = cnv.id;
                    console.log(updChat);
                    vm.convos = _.findWhere(vm.chats, {id:cnv.id });
                    console.log(vm.convos);
                    updChat = _.omit(updChat, 'users');
                    sendFn(updChat);
                }else{
                    vm.match = false;
                }
            })
            if(!vm.match){
                sendFn(updChat);
            }         
        }else{
            chat.chatid = convo_id;
            console.log(chat);
            var updChat = chat;
            sendFn(updChat);
        }

    }

    function sendFn(updChat){
        Messages.sendChat(updChat)
            .then(sendChatSuccess)
            .catch(sendChatError);
    }

    function sendChatSuccess(response){
        console.log(response);
        vm.chat = {};
    }

    function sendChatError(errorMsg){
        console.log(errorMsg);
    }

    vm.getConv = function(chat){
        console.log(chat);
        
        if(!chat){
            vm.convos = {};
        }else{
            // vm.convos = {};
            vm.convos = _.findWhere(vm.chats, {id: chat.id});
            console.log(vm.convos);
            console.log(vm.convos.chat_group[0].id);
            vm.chatId = vm.convos.chat_group[0].id;
            vm.messageViewed(vm.chatId);
            // vm.convos
            // vm.messageViewed(chat_id);
            // var msgDates = [];
            // angular.forEach(chat.chat_group, function(val,key){
            //     console.log(val)
            //     var msg = {}
            //     msg.push(val.id);
            //     msg.push(val.chat_message_created);
            //     console.log(msg);
            // });
            // console.log(msgDates);

                   
        }

    }



    vm.messageViewed = function(chatId){
        vm.chatViewed = {};
        vm.chatViewed['chatid'] = chatId;
        vm.chatViewed['chat_viewed'] = true;
        console.log(vm.chatViewed);
        // Messages.chatViewed(chatId, vm.chatViewed)
        //     .then(messageViewedSuccess)
        //     .catch(messageViewedError);
    }

    function messageViewedSuccess(response){
        console.log(response);
    }

    function messageViewedError(errorMsg){
        console.log(errorMsg);
    }

    $scope.chatMessageChannel = 'chat-message'
    $dragon.onReady(function() {
        $dragon.subscribe('chat-message', $scope.chatMessageChannel, {}).then(function(response) {
                // $scope.dataMapper = new DataMapper(response.data);
                console.log(response);
        });
    });

    $dragon.onChannelMessage(function(channels, message) {

        if (indexOf.call(channels, $scope.chatMessageChannel) > -1) {
            $scope.$apply(function() {
                // $scope.dataMapper.mapData(vm.messages, message);
                console.log(message.data._type, message);
            
                console.log(vm.chats);
                vm.tmpChat = _.findWhere(vm.chats, {id:message.data.chat.id});
                vm.chatGroup = _.omit(message.data, 'chat');
                console.log('vm chat grp', vm.chatGroup);
                if(vm.tmpChat){
                    console.log('in chats', vm.tmpChat)
                    vm.tmpChat['chat_group'].unshift(vm.chatGroup);
                    console.log('add to chats', vm.tmpChat)
                }else{
                    console.log('not in chats', vm.tmpChat)
                    vm.tmpObj = {}
                    vm.tmpObj = message.data.chat;
                    vm.tmpObj['chat_group'] = [];
                    vm.tmpObj['chat_group'].push(vm.chatGroup);
                    console.log('tmpObj', vm.tmpObj);
                    vm.chats.unshift(vm.tmpObj);
                    vm.convos = vm.tmpObj;
                }
                console.log(vm.chats);

            });
        }
    });

  }
})();