from django.contrib import admin
from orders.models import Order, Comment, ReqItem, ReqProduct, ReqFile, Offer, OfferItem, Good, Detail

class DetailInline(admin.StackedInline):
    model = Detail
    extra = 0
    list_display = ('id', 'good_info', 'good_description',)

class OptizAdmin(admin.ModelAdmin):

    inlines = [
        DetailInline,
    ]
    list_display = ('id', 'domain', 'family', 'subfamily',)
    ordering = ('domain',)
    filter_horizontal = ()

admin.site.register(Good, OptizAdmin)

class ReqItemInline(admin.StackedInline):
    model = ReqItem
    extra = 0

class ReqProdInline(admin.StackedInline):
    model = ReqProduct
    extra = 0

class OfferInline(admin.StackedInline):
    model = Offer
    extra = 0

class OfferItemInline(admin.StackedInline):
    model = OfferItem
    extra = 0

class ReqFileInline(admin.StackedInline):
    model = ReqFile
    extra = 0

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

class OrderAdmin(admin.ModelAdmin):

    inlines = [
        ReqItemInline,
        OfferInline,
        CommentInline,
    ]
    list_display = ('order_number', 'order_company', 'order_created',)
    ordering = ('-order_number',)
        
admin.site.register(Order, OrderAdmin)

class ReqItemAdmin(admin.ModelAdmin):

    inlines = [
        ReqProdInline,
        ReqFileInline,
    ]

    list_display = ('get_order_num', 'item_subfam', 'get_order_company',)
    ordering = ('-order',)

admin.site.register(ReqItem, ReqItemAdmin)

class ReqFileAdmin(admin.ModelAdmin):
    class Meta:
        model = ReqFile
        
admin.site.register(ReqFile, ReqFileAdmin)

class OfferAdmin(admin.ModelAdmin):

    inlines = [
        OfferItemInline,
    ]

    list_display = ('get_order_num', 'offer_version', 'get_order_company', 'offer_created', 'offer_approval_status',)
    ordering = ('-order', 'offer_version',)

admin.site.register(Offer, OfferAdmin)

