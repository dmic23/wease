from django.utils import timezone
from datetime import date
from rest_framework import serializers
from rest_framework.parsers import JSONParser
import json
from eventlog.models import Log
from messaging.models import Mail, MailReply, MailFile, Chat, ChatMessage
from authentication.models import Account, Company
from authentication.serializers import UserCompanySerializer
from orders.serializers import OrderSerializer


class LogSerializer(serializers.ModelSerializer):
    user = UserCompanySerializer()
    company_name = serializers.CharField(source='company.name', required=False)
    not_action = serializers.CharField(required=False)
    content_type = serializers.StringRelatedField(required=False) 

    class Meta:
        model = Log
        fields = ('id', 'timestamp', 'user', 'company', 'company_name', 'not_action', 'content_type', 'object_id',
				'notification', 'extra',)

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        instance.viewed_by.add(user)
        instance.save()

        return instance


class MailFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MailFile
        fields = ('base_mail', 'reply_mail', 'file_created', 'mail_file',)


class MailReplySerializer(serializers.ModelSerializer):
    orig_mail = serializers.StringRelatedField(required=False)
    reply_files = MailFileSerializer(required=False, many=True)
    reply_read_by = UserCompanySerializer(required=False, many=True)
    trash = UserCompanySerializer(required=False, many=True)
    mail_to = UserCompanySerializer(required=False, many=True)
    reply_created_by = UserCompanySerializer(required=False)

    class Meta:
        model = MailReply
        fields = ('id', 'orig_mail', 'subject', 'body', 'reply_draft', 'reply_read_date', 'reply_read_by',
                'trash', 'mail_to', 'reply_created_by', 'reply_created', 'reply_files',)

    def create(self, validated_data):
        print "val data === %s" % validated_data

        return validated_data['reply_mail']

class MailSerializer(serializers.ModelSerializer):
    reply_mail = MailReplySerializer(required=False, many=True)
    base_files = MailFileSerializer(required=False, many=True)
    mail_read_by = UserCompanySerializer(required=False, many=True)
    trash = UserCompanySerializer(required=False, many=True)
    mail_to = UserCompanySerializer(required=False, many=True)
    mail_created_by = UserCompanySerializer(required=False)

    class Meta:
        model = Mail
        fields = ('id', 'subject', 'body', 'mail_draft', 'mail_read', 'mail_read_date', 'mail_read_by', 'trash', 'mail_to',
                'mail_created_by', 'mail_created', 'reply_mail', 'base_files',)

    def create(self, validated_data):
        return validated_data['mail']

    def update(self, instance, validated_data):
        print "SELF == %s " % self
        print "instance === %s" % instance
        print "validated Data === %s" % validated_data
        mail_to_all = validated_data.pop('mailTo')
        print "UPD MTA --- %s" % mail_to_all
        for mtu in instance.mail_to.all():
            print "UPD MTU --- %s" % mtu
            if not mtu.id in mail_to_all:
                print "remove mtu --- %s" % mtu
                instance.mail_to.remove(mtu)
        for mt in mail_to_all:
            print "MT --- %s" % mt
            if not instance.mail_to.all().filter(id=mt).exists():
                mail_to_user = Account.objects.get(id=mt)
                instance.mail_to.add(mail_to_user)
        print "INST MT -- %s" %instance.mail_to.all()
        instance.subject = validated_data.get('subject', instance.subject)
        instance.body = validated_data.get('body', instance.body)
        instance.mail_draft = validated_data.get('mail_draft', instance.mail_draft)
        instance.mail_read = validated_data.get('mail_read', instance.mail_read)
        instance.mail_read_date = validated_data.get('mail_read_date', instance.mail_read_date)
        instance.trash = validated_data.get('trash', instance.trash)
        instance.save()

        return instance

class ChatMessageSerializer(serializers.ModelSerializer):
    chat = serializers.StringRelatedField(required=False)
    user = UserCompanySerializer(required=False)
    chat_viewed = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = ChatMessage
        fields = ('id', 'chat', 'user', 'chat_message_created', 'chat_message', 'chat_viewed',)

    def create(self, validated_data):
        chat_msg = ChatMessage.objects.create(**validated_data)
        print "SELF SER CHAT M== %s" %self
        print "VALD DATA CHAT ms === %s" %validated_data
        return chat_msg

    def update(self, instance, validated_data):
        instance.save()
        return instance

class ChatSerializer(serializers.ModelSerializer):
    users = UserCompanySerializer(many=True)
    chat_user = serializers.PrimaryKeyRelatedField(source='users', read_only=True, required=False, many=True)
    chat_group = ChatMessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'users', 'chat_user', 'chat_group',)
