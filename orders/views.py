from rest_framework import permissions, viewsets, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import list_route, api_view, detail_route
from orders.models import Good, Detail, Order, ReqItem, ReqProduct, ReqFile, Offer, OfferItem, Comment
from authentication.models import Address
from orders.serializers import OrderSerializer, OrderSimpleSerializer, GoodSerializer, DetailSerializer, ReqItemSerializer, ReqProductSerializer, ReqFileSerializer, OfferSerializer, OfferItemSerializer, CommentSerializer
from operator import itemgetter, attrgetter
from django.utils import timezone
from datetime import date

class OrderViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def list(self, request, order_id=None):
        if self.request.user.optiz:
            queryset = Order.objects.all()
        else:
            queryset = self.queryset.filter(order_company=self.request.user.user_company)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        instance = serializer.save(order_created_by=self.request.user, order_company=self.request.user.user_company, order_status_change_date=timezone.now())
        return super(OrderViewSet, self).perform_create(serializer)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user, **self.request.data)

class OrderSimpleViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Order.objects.all()
    serializer_class = OrderSimpleSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def list(self, request, order_id=None):
        if self.request.user.optiz:
            queryset = Order.objects.filter(order_company__company_assigned_to=self.request.user)
        else:
            queryset = self.queryset.filter(order_company=self.request.user.user_company)
        serializer = OrderSimpleSerializer(queryset, many=True)
        return Response(serializer.data)

class OrderApvViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Order.objects.all()
    serializer_class = OrderSimpleSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def list(self, request, order_id=None):
        if self.request.user.optiz:
            queryset = Order.objects.filter(order_company__company_assigned_to=self.request.user).filter(order_status__in=['APN','OFR'])
        else:
            queryset = self.queryset.filter(order_company=self.request.user.user_company).filter(order_status__in=['APN','OFR'])
        serializer = OrderSimpleSerializer(queryset, many=True)
        return Response(serializer.data)

class ReqItemViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = ReqItem.objects.all()
    serializer_class = ReqItemSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            if self.request.data['add']:
                order_id = int(self.request.data['order_id'])
                order = Order.objects.get(id=order_id)
            else:
                order = Order.objects.create(order_created_by=user, order_company=user.user_company, order_status_change_date=timezone.now())
                yr = str(date.today().year)[2:]
                order.order_number = ''.join(["0",yr,str(order.id)])
                order.order_version = 00
                order.order_draft = True
                order.order_status = 'WRQ'
                order.company_approval_status = 'WRQ'
                order.optiz_status = 'WRQ'

            order.save()
            serializer.save(order=order, user=user, **self.request.data)
            # return super(ReqItemViewSet, self).perform_create(serializer)

    def perform_update(self, serializer):
        if serializer.is_valid(raise_exception=True):
            user = self.request.user
            val_data = self.request.data['data']
            order = Order.objects.get(id=val_data['order'])

            serializer.save(order=order, user=user, **self.request.data)

class ReqProductViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = ReqProduct.objects.all()
    serializer_class = ReqProductSerializer

    def list(self, request, reqitem_id=None):
        queryset = self.queryset.filter(req_item=reqitem_id)
        serializer = ReqProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None, reqitem_id=None):
        queryset = self.queryset.get(id=id, req_item=reqitem_id)
        serializer = ReqProductSerializer(queryset)
        return Response(serializer.data)

class ReqFileViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = ReqFile.objects.all()
    serializer_class = ReqFileSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        rqi = self.kwargs['reqitem_id']
        r_file = self.request.data['file']
        instance = serializer.save(req_item=ReqItem.objects.get(id=rqi), req_file=r_file)
        return super(ReqFileViewSet, self).perform_create(serializer)

class RequestViewSet(viewsets.ViewSet):
    queryset = ReqItem.objects.all()

    def list(self, request, order_id=None):
        queryset = self.queryset.filter(order=order_id)
        serializer = ReqItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, order_id=None):
        queryset = self.queryset.get(pk=pk, order=order_id)
        serializer = ReqItemSerializer(queryset)
        return Response(serializer.data)

class OfferViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def list(self, request, order_id=None):
        queryset = self.queryset.filter(order=order_id)
        serializer = OfferSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None, order_id=None):
        queryset = self.queryset.get(id=id, order=order_id)
        serializer = OfferSerializer(queryset)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user, **self.request.data)

class OfferItemViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = OfferItem.objects.all()
    serializer_class = OfferItemSerializer

    def retrieve(self, request, id=None):
        queryset = self.queryset.get(id=id)
        serializer = OfferItemSerializer(queryset)
        return Response(serializer.data)

class GoodViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Good.objects.all()
    serializer_class = GoodSerializer

class CommentViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class DetailViewSet(viewsets.ViewSet):
    lookup_field = 'good'
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer

    def list(self, request, good_id=None):
        queryset = self.queryset.filter(good=good_id)
        serializer = DetailSerializer(queryset, many=True)
        return Response(serializer.data)




