from django.db.models import Q
from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter, ModelPubRouter
from messaging.models import Mail, MailReply, Chat, ChatMessage
from eventlog.models import Log
from messaging.dragon_serializers import MailSerializer, MailReplySerializer, EventLogSerializer, ChatSerializer, ChatMessageSerializer


class MailRouter(ModelRouter):
    route_name = 'mail'
    serializer_class = MailSerializer
    include_related = [MailReplySerializer, MailReplySerializer]
    model = Mail

    def get_object(self, **kwargs):
        print "self obj -- %s" % self
        print "kwargs obj === %s" % kwargs
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        print "self -- %s" % self
        print "kwargs === %s" % kwargs
        return self.model.objects.all()
        # return self.model.objects.filter(Q(mail_to=self.request.user) | Q(mail_created_by=self.request.user)).exclude(Q(mail_draft=True), ~Q(mail_created_by=self.request.user)).distinct()

class MailReplyRouter(ModelRouter):
    route_name = 'mail-reply'
    serializer_class = MailReplySerializer
    model = MailReply

    def get_object(self, **kwargs):
        print "self obj reply -- %s" % self
        print "kwargs obj reply === %s" % kwargs
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        print "self reply -- %s" % self
        print "kwargs reply === %s" % kwargs
        # return self.model.objects.filter(orig_mail__id=kwargs['list_id'])
        return self.model.objects.all()

class NotificationRouter(ModelRouter):
    route_name = 'notification'
    serializer_class = EventLogSerializer
    model = Log

    def get_object(self, **kwargs):
        print "self obj reply -- %s" % self
        print "kwargs obj reply === %s" % kwargs
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        print "self reply -- %s" % self
        print "kwargs reply === %s" % kwargs
        return self.model.objects.all()

class ChatRouter(ModelRouter):
    route_name = 'chat'
    serializer_class = ChatSerializer
    include_related = [ChatMessageSerializer, ChatMessageSerializer]
    model = Chat

    def get_object(self, **kwargs):
        print "self obj -- %s" % self
        print "kwargs obj === %s" % kwargs
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        print "self -- %s" % self
        print "kwargs === %s" % kwargs
        return self.model.objects.all()

class ChatMessageRouter(ModelRouter):
    route_name = 'chat-message'
    serializer_class = ChatMessageSerializer
    # include_related = [ChatSerializer, ChatSerializer]
    model = ChatMessage

    def get_object(self, **kwargs):
        print "self obj -- %s" % self
        print "kwargs obj === %s" % kwargs
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        print "self -- %s" % self
        print "kwargs === %s" % kwargs
        return self.model.objects.all()

route_handler.register(MailRouter)
route_handler.register(MailReplyRouter)
route_handler.register(NotificationRouter)
route_handler.register(ChatRouter)
route_handler.register(ChatMessageRouter)

