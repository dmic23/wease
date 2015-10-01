from django.contrib import admin
from messaging.models import Mail, MailReply, MailFile, Chat, ChatMessage


class MailFileInline(admin.StackedInline):
    model = MailFile
    extra = 0

class MailReplyInline(admin.StackedInline):
    model = MailReply
    extra = 0

class MailAdmin(admin.ModelAdmin):

    inlines = [
        MailReplyInline,
        MailFileInline,
    ]
    list_display = ('mail_created', 'mail_created_by', 'subject',)
    list_filter = ('mail_created', 'mail_created_by',)
    ordering = ('-mail_created',)
    filter_horizontal = ()

class ChatMessageInline(admin.StackedInline):
    model = ChatMessage
    extra = 0
    list_display = ('id', 'user', 'chat', 'chat_message_created', 'chat_message', )

class ChatAdmin(admin.ModelAdmin):

    inlines = [
        ChatMessageInline,
    ]
    list_display = ('id', )
    filter_horizontal = ()
        
admin.site.register(Mail, MailAdmin)
admin.site.register(Chat, ChatAdmin)
