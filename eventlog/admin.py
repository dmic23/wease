from django.contrib import admin

from eventlog.models import Log

class LogAdmin(admin.ModelAdmin):
    class Meta:
        model = Log
    list_display = ('timestamp', 'company', 'user', 'not_action', 'extra',)
    list_filter = ('timestamp', 'company', 'user', 'not_action',)
    ordering = ('-timestamp',)
    filter_horizontal = ()
    
admin.site.register(Log, LogAdmin)
