from django.conf.urls import include, patterns, url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_nested import routers
from authentication.views import AccountViewSet, CompanyViewSet, AddressViewSet, LoginView, LogoutView, OptizViewSet
from orders.views import OrderViewSet, OrderSimpleViewSet, OrderApvViewSet, GoodViewSet, DetailViewSet, RequestViewSet, ReqItemViewSet, ReqProductViewSet, ReqFileViewSet, OfferViewSet, OfferItemViewSet
from wease.views import IndexView
from messaging.views import OrderActivityViewSet, NotificationViewSet, MailViewSet, MailReplyViewSet, MailFileViewSet, ChatViewSet, ChatMessageViewSet
import settings
from django.contrib import admin

admin.autodiscover()

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'req-items', ReqItemViewSet)
router.register(r'offers', OfferViewSet)
router.register(r'order-simple', OrderSimpleViewSet)
router.register(r'order-apv', OrderApvViewSet)
router.register(r'offer-items', OfferItemViewSet)
router.register(r'goods', GoodViewSet)
router.register(r'optiz', OptizViewSet)
router.register(r'order-activity', OrderActivityViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'mail', MailViewSet)
router.register(r'chat', ChatViewSet)
router.register(r'chat-message', ChatMessageViewSet)

accounts_router = routers.NestedSimpleRouter(
    router, r'accounts', lookup='account',
)
accounts_router = routers.NestedSimpleRouter(
    router, r'companies', lookup='company',
)
accounts_router = routers.NestedSimpleRouter(
    router, r'addresses', lookup='address',
)
goods_router = routers.NestedSimpleRouter(
    router, r'goods', lookup='good',
)
orders_router = routers.NestedSimpleRouter(
    router, r'orders', lookup='order',
)
order_simple_router = routers.NestedSimpleRouter(
    router, r'order-simple', lookup='orders',
)
order_apv_router = routers.NestedSimpleRouter(
    router, r'order-apv', lookup='order',
)
req_router = routers.NestedSimpleRouter(
    router, r'req-items', lookup='reqitem',
)
offer_router = routers.NestedSimpleRouter(
    router, r'offer-items', lookup='offeritem',
)
optiz_router = routers.NestedSimpleRouter(
    router, r'optiz', lookup='optiz',
)
order_activity_router = routers.NestedSimpleRouter(
    router, r'order-activity', lookup='object_id',
)
notification_router = routers.NestedSimpleRouter(
    router, r'notifications', lookup='id',
)
mail_router = routers.NestedSimpleRouter(
    router, r'mail', lookup='mail',
)
chat_router = routers.NestedSimpleRouter(
    router, r'chat', lookup='chat',
)
chat_message_router = routers.NestedSimpleRouter(
    router, r'chat-message', lookup='chat_message',
)

orders_router.register(r'requests', RequestViewSet)
orders_router.register(r'offers', OfferViewSet)
req_router.register(r'req-prods', ReqProductViewSet)
req_router.register(r'req-files', ReqFileViewSet)
offer_router.register(r'item', OfferItemViewSet)
goods_router.register(r'details', DetailViewSet)
mail_router.register(r'mail-reply', MailReplyViewSet)
mail_router.register(r'mail-file', MailFileViewSet)

urlpatterns = patterns(
    '',

    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(accounts_router.urls)),
    url(r'^api/v1/', include(goods_router.urls)),
    url(r'^api/v1/', include(orders_router.urls)),
    url(r'^api/v1/', include(req_router.urls)),
    url(r'^api/v1/', include(offer_router.urls)), 
    url(r'^api/v1/', include(order_simple_router.urls)),
    url(r'^api/v1/', include(order_apv_router.urls)), 
    url(r'^api/v1/', include(optiz_router.urls)),
    url(r'^api/v1/', include(order_activity_router.urls)), 
    url(r'^api/v1/', include(notification_router.urls)), 
    url(r'^api/v1/', include(mail_router.urls)),  
    url(r'^api/v1/', include(chat_router.urls)),        
    url(r'^api/v1/', include(chat_message_router.urls)),  
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    url(r'^reset_password/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^reset_password_done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),    
    url(r'^$',  IndexView.as_view(), name='index'),    
    url(r'^/$',  IndexView.as_view(), name='index'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
   # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
   
    urlpatterns += staticfiles_urlpatterns()

