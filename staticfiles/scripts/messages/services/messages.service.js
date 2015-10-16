(function () {
    'use strict';

    angular
        .module('messages.services')
        .factory('Messages', Messages);

    Messages.$inject = ['$http', '$q', '$timeout'];

    function Messages($http, $q, $timeout) {

        var Messages = {
            orderActivity: orderActivity,
            getNotifications: getNotifications,
            notificationViewed: notificationViewed,
            getAllMessages: getAllMessages,
            getSingleMessage: getSingleMessage,  
            getAllMail: getAllMail,
            newMessage: newMessage,
            updateMessage: updateMessage,
            replyMessage: replyMessage,
            getChats:getChats,
            sendChat:sendChat,
            chatViewed:chatViewed,
        };

        return Messages;

        function generalCallbackSuccess(response){
            return response.data;
        }

        function generalCallbackError(response){
            console.log(response)
            return $q.reject('Error '+response.status+'');
        }

        function orderActivity(orderId) {
            return $http.get('/api/v1/order-activity/'+orderId+'/')
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }    

        function getNotifications() {
            return $http.get('/api/v1/notifications/')
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }

        function notificationViewed(notId){
            return $http.put('/api/v1/notifications/'+notId+'/')
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);            
        }

        function getAllMail(user){
            return $http.get('api/v1/mail/')
                .then((function (user){
                    return function (response){
                        console.log(user, response);
                        Messages.allMessages = {};
                        Messages.allMessages.inbox = [];
                        Messages.allMessages.sent = [];
                        Messages.allMessages.draft = [];
                        Messages.allMessages.trash = [];
                        angular.forEach(response.data, function (v, k, o){
                            if(v.mail_created_by.username === user.username){
                                if(v.mail_draft === false){
                                    Messages.allMessages.sent.push(v);
                                    if(v.reply_mail.length > 0){
                                        angular.forEach(v.reply_mail, function (val, key, obj){
                                            angular.forEach(val.mail_to, function (va, ke, ob){
                                                if(va.username === user.username){
                                                    if(!_.contains(Messages.allMessages.inbox, v)){
                                                        Messages.allMessages.inbox.push(v);
                                                    }
                                                }
                                            })
                                        })                                         
                                    }
                                }
                            }
                            if(v.mail_draft === true){
                                Messages.allMessages.draft.push(v);
                            }
                            if(v.trash === true){
                                Messages.allMessages.trash.push(v);
                            }
                            angular.forEach(v.mail_to, function (val, key, obj){
                                if(val.username === user.username){
                                    if(!_.contains(Messages.allMessages.inbox, v)){
                                        Messages.allMessages.inbox.push(v);
                                    }
                                }
                            })
                        })
                        return Messages.allMessages;
                    }
                })(user))
                .catch(generalCallbackError);
        }

        function getAllMessages(){
            return $timeout(function() {
                return Messages.allMessages; 
            }, 1000);
        }

        function getSingleMessage(mailId){
            return $http.get('api/v1/mail/'+mailId+'/')
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }

        function newMessage(msg){
            return $http.post('api/v1/mail/', msg)
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }

        function updateMessage(msgId, msg){
            return $http.put('api/v1/mail/'+msgId+'/', msg)
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }

        function replyMessage(msgId, replyMsg){
            return $http.post('api/v1/mail/'+msgId+'/mail-reply/', replyMsg)
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }

        function getChats(){
            return $http.get('api/v1/chat/')
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }

        function sendChat(chat){
            return $http.post('api/v1/chat-message/', chat)
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }

        function chatViewed(chatid, chat){
            return $http.put('api/v1/chat-message/'+chatid+'/', chat)
                .then(generalCallbackSuccess)
                .catch(generalCallbackError);
        }

    }
})();
