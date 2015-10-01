import json
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, status, viewsets, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import list_route, api_view, detail_route
from authentication.models import Account
from orders.models import Order
from eventlog.models import Log, log
from messaging.models import Mail, MailReply, Chat, ChatMessage
from messaging.serializers import LogSerializer, MailSerializer, MailReplySerializer, ChatSerializer, ChatMessageSerializer
from django.utils import timezone
from datetime import date

from swampdragon.pubsub_providers.data_publisher import publish_data


class OrderActivityViewSet(viewsets.ModelViewSet):
    lookup_field = 'object_id'
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def list(self, request, logs=None):
        queryset = self.queryset.filter(content_type=11)
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None, object_id=None): 
        ct = ContentType.objects.get_for_model(Order)  
        print "CONT TYPE --- %s" %ct 
        queryset = self.queryset.filter(object_id=object_id).filter(content_type=ct)
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)

class NotificationViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Log.objects.filter(notification=True)
    serializer_class = LogSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def list(self, request, notification=None):
        if self.request.user.optiz:
            queryset = self.queryset.filter(company__company_assigned_to=self.request.user).exclude(viewed_by=self.request.user)
        else:
            queryset = self.queryset.filter(company=self.request.user.user_company).exclude(viewed_by=self.request.user)
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):      
        queryset = self.queryset.filter(id=id, notification=True)
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user, **self.request.data)

class MailViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Mail.objects.all()
    serializer_class = MailSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def list(self, request, mail=None):
        queryset = self.queryset.filter(Q(mail_to=self.request.user) | Q(mail_created_by=self.request.user) | Q(reply_mail__mail_to=self.request.user)).exclude(Q(mail_draft=True), ~Q(mail_created_by=self.request.user)).distinct()
        print "MAIL QUERY SET ==== %s" % queryset
        serializer = MailSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            mail_to_all = self.request.data.pop('mailTo')
            print "MTA --- %s" % mail_to_all
            mail = Mail.objects.create(mail_created_by=user, **self.request.data)
            for mt in mail_to_all:
                print "MT --- %s" % mt
                mail_to_user = Account.objects.get(id=mt)
                mail.mail_to.add(mail_to_user)
            mail.save()
            serializer.save(mail=mail)

    def perform_update(self, serializer):
        if serializer.is_valid():
            user = self.request.user

            serializer.save(user=user, **self.request.data)

class MailReplyViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = MailReply.objects.all()
    serializer_class = MailReplySerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def list(self, request, mail_id=None):
        queryset = self.queryset.filter(orig_mail=mail_id)
        serializer = MailReplySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None, mail_id=None):
        queryset = self.queryset.get(id=id, orig_mail=mail_id)
        serializer = MailReplySerializer(queryset)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            mail_to_all = self.request.data.pop('mail_to')
            mail_id = self.request.data.pop('id')
            orig_mail = Mail.objects.get(id=mail_id)
            reply_mail = MailReply.objects.create(reply_created_by=user, orig_mail=orig_mail)
            print "MAIL CREATED BY == %s" % self.request.data['mail_created_by']
            if 'mail_created_by' in self.request.data and user.id != self.request.data['mail_created_by']:
                print "MAIL CREATED 2 == %s" % self.request.data['mail_created_by']
                mcb = self.request.data.pop('mail_created_by')
                mcu = Account.objects.get(id=mcb)
                reply_mail.mail_to.add(mcu)
            print "MTA --- %s" % mail_to_all
            for mt in mail_to_all:
                print "MT --- %s" % mt
                if user.id != mt['id']:
                    mail_to_user = Account.objects.get(id=mt['id'])
                    reply_mail.mail_to.add(mail_to_user)
            reply_mail.subject = self.request.data['subject']
            reply_mail.body = self.request.data['body']
            reply_mail.save()
            serializer.save(reply_mail=reply_mail, **self.request.data)

class ChatViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def list(self, request):
        queryset = self.queryset.filter(users=self.request.user)
        serializer = ChatSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = self.queryset.get(id=id)
        serializer = ChatSerializer(queryset)
        return Response(serializer.data)

class ChatMessageViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def list(self, request):
        queryset = self.queryset.filter(user=self.request.user)
        serializer = ChatMessageSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = self.queryset.get(id=id)
        serializer = ChatMessageSerializer(queryset)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            if 'users' in self.request.data:
                chatters = self.request.data.pop('users')
            if 'chatid' in self.request.data:
                chatid = self.request.data.pop('chatid')
                chat = Chat.objects.get(id=chatid)
            else:
                chat = Chat.objects.create()
                for cu_id in chatters:
                    chat_user = Account.objects.get(id=cu_id)
                    chat.users.add(chat_user)
                chat.users.add(user)
            
            serializer.save(user=user, chat=chat, chat_message_created=timezone.now(), **self.request.data)

    def perform_update(self, serializer):
        if serializer.is_valid():
            if 'chat_viewed' in self.request.data:
                cv = self.request.data.pop('chat_viewed')
                chatid = self.request.data.pop('chatid')
                chat_msg = ChatMessage.objects.get(id=chatid)
                chat_msg.chat_viewed.add(self.request.user)

                serializer.save()





