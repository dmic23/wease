# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.encoding import smart_unicode
from authentication.models import Account, Company, Address, get_upload_file_name
from swampdragon.models import SelfPublishModel
from messaging.dragon_serializers import MailSerializer, MailReplySerializer, ChatSerializer, ChatMessageSerializer
from time import time
from wease import settings


class Mail(SelfPublishModel, models.Model):
    subject = models.CharField(max_length=250, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    mail_draft = models.BooleanField(default=False)
    mail_read = models.BooleanField(default=False)
    mail_read_by = models.ManyToManyField(Account, related_name='mail_read_by', blank=True)
    trash = models.ManyToManyField(Account, related_name='mail_trash_by', blank=True)
    mail_to = models.ManyToManyField(Account, related_name='mail_sent_to', blank=True)
    mail_created_by = models.ForeignKey(Account, related_name='mail_created_by_user')
    mail_created = models.DateTimeField(auto_now_add=True)
    serializer_class = MailSerializer
    
    def __unicode__(self):
        return smart_unicode(self.subject)
    
        
class MailReply(SelfPublishModel, models.Model):
    orig_mail = models.ForeignKey(Mail, related_name='reply_mail')
    subject = models.CharField(max_length=250, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    reply_draft = models.BooleanField(default=False)    
    reply_read_by = models.ManyToManyField(Account, related_name='reply_read_by', blank=True)
    trash = models.ManyToManyField(Account, related_name='reply_trash_by', blank=True)
    mail_to = models.ManyToManyField(Account, related_name='reply_sent_to', blank=True)
    reply_created_by = models.ForeignKey(Account, related_name='reply_created_by_user')
    reply_created = models.DateTimeField(auto_now_add=True)
    serializer_class = MailReplySerializer
    
    def __unicode__(self):
        return smart_unicode(self.orig_mail, self.id)
    
class MailFile(models.Model):
    base_mail = models.ForeignKey(Mail, related_name='base_files', blank=True, null=True)
    reply_mail = models.ForeignKey(MailReply, related_name='reply_files', blank=True, null=True)
    file_created = models.DateTimeField(auto_now=True)
    mail_file = models.FileField(upload_to=get_upload_file_name, null=True, blank=True)

class Chat(SelfPublishModel, models.Model):
    users = models.ManyToManyField(Account, related_name='chat_users')
    serializer_class = ChatSerializer

    def __unicode__(self):
        return smart_unicode(self.id)

class ChatMessage(SelfPublishModel, models.Model):
    chat = models.ForeignKey(Chat, related_name='chat_group')
    user = models.ForeignKey(Account, related_name='chat_user')
    chat_message_created = models.DateTimeField(auto_now_add=True)
    chat_message = models.TextField(blank=True, null=True)
    chat_viewed = models.ManyToManyField(Account, related_name='chat_viewed')
    serializer_class = ChatMessageSerializer

    class Meta:
        ordering = ['-chat_message_created']

    def __unicode__(self):
        return smart_unicode(self.chat_message_created)

