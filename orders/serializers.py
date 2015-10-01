# -*- coding: utf-8 -*-
from django.forms import widgets
from django.utils import timezone
from datetime import date
from rest_framework import serializers
from rest_framework.parsers import JSONParser
import json
from collections import *
from authentication.models import Account, Company, Address
from orders.models import Order, ReqItem, ReqProduct, ReqFile, Offer, OfferItem, Comment, Good, Detail
from authentication.serializers import AccountSerializer, UserCompanySerializer, CompanySerializer, AddressSerializer
from eventlog.models import log

class CommentSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username')
    created_by_first_name = serializers.CharField(source='created_by.first_name')
    created_by_last_name = serializers.CharField(source='created_by.last_name')
    created_by_pic = serializers.CharField(source='created_by.user_pic')

    class Meta:
        model = Comment
        fields = ('id', 'created_by', 'created_by_username', 'created_by_first_name', 'created_by_last_name', 'created_by_pic', 'order', 'body', 'created_date',)


class OfferItemSerializer(serializers.ModelSerializer):
    offer = serializers.CharField(required=False)

    class Meta:
        model = OfferItem
        fields = ('id', 'offer', 'item_name', 'item_details', 'price', 'item_sub_total', 'frequency', 'quantity',
            'delivery_date', 'date_start', 'date_end',)


class OfferSerializer(serializers.ModelSerializer):
    order = serializers.CharField(required=False)
    offer_item = OfferItemSerializer(many=True, required=False)
    offer_terms = serializers.CharField(required=False, allow_blank=True)
    offer_created_by = serializers.CharField(required=False)
    offer_created_by_name = serializers.CharField(source='offer_created_by.get_full_name', required=False)
    offer_approval_display = serializers.CharField(source='get_offer_approval_status_display', required=False)
    offer_approval_by = serializers.CharField(required=False)
    offer_approval_by_name = serializers.CharField(source='offer_approval_by.get_full_name', required=False)    

    class Meta:
        model = Offer
        fields = ('id', 'order', 'offer_version', 'offer_domain', 'offer_total', 'offer_terms',
            'offer_created', 'offer_created_by', 'offer_created_by_name', 'offer_approval_status', 'offer_approval_display', 'offer_approval', 'offer_approval_by', 'offer_approval_by_name', 'offer_item',)

    def create(self, validated_data):
        user = validated_data['user']
        if 'blank_offer' in validated_data:
            company = Company.objects.get(id=validated_data['offer_company'])
            address = Address.objects.get(id=validated_data['delivery_address'])
            order = Order.objects.create(order_company=company, delivery_address=address, order_created_by=user, order_status_change_date = timezone.now())
            yr = str(date.today().year)[2:]
            order.order_number = ''.join(["0",yr,str(order.id)])
            order.order_version = 01
            if 'reference_number' in validated_data:
                order.reference_number = validated_data['reference_number']
        else:
            order = Order.objects.get(id=validated_data['order'])
            order.order_status_change_date = timezone.now()
        if order.offer_version >= 01:
            order.order_version = order.order_version+1
        order.offer_version = order.offer_version+1
        order.order_offer = True
        order.order_total = validated_data['offer_total']
        order.modified_by = user
        order.order_status_change_by = user
        order.order_status = 'OFR'
        order.optiz_status = 'OSB'
        order.optiz_status_change_by = user
        order.optiz_status_change_date = timezone.now()
        order.save()
        offer = Offer.objects.create(order=order, offer_version=order.offer_version, offer_created_by=user, offer_total=validated_data['offer_total'], offer_terms=validated_data['offer_terms'], offer_domain=validated_data['offer_domain'])
        offer.save()
        for item in validated_data['offer_item']:
            offer_item = OfferItem(offer=offer, **item)
            offer_item.save()
        log(
            user=user,
            company=order.order_company,
            not_action='offer created',
            obj=order,
            notification=True,
            extra={
                'order_id':order.id,
                'order_number':order.order_number,
                'order_version':order.offer_version,
                'offer_total':offer.offer_total,
                'order_status':order.order_status,
                'order_status_full':order.get_order_status_display(),
            }
        )
        return offer


class ReqFileSerializer(serializers.ModelSerializer):
    req_item = serializers.CharField(required=False)

    class Meta:
        model = ReqFile
        fields = ('id', 'req_item', 'file_created', 'req_file',)


class ReqProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReqProduct
        fields = ('id', 'req_item', 'prod_fam', 'prod_subfam', 'prod_title', 'prod_details', 'prod_description',)


class ReqItemSerializer(serializers.ModelSerializer):
    good = serializers.CharField(source='good.id', required=False)
    order = serializers.CharField(required=False)
    order_draft = serializers.BooleanField(source='order.order_draft', required=False)
    item_details = serializers.CharField(required=False)
    req_product = ReqProductSerializer(many=True, required=False)
    req_item_file = ReqFileSerializer(many=True, required=False)

    class Meta:
        model = ReqItem
        fields = ('id', 'good', 'order', 'order_draft', 'req_domain', 'item_fam', 'item_subfam', 'item_details', 'req_product', 'req_item_file',)

    def create(self, validated_data):
        order = validated_data.pop('order')
        goods = validated_data.pop('good')
        user = validated_data['user']
        good = Good.objects.get(id=validated_data['good_id'])
        if 'item_details' in validated_data:
            item_details = validated_data.pop('item_details')
        else:
            item_details = ''
        order.order_draft = validated_data['order_draft']
        order.save()
        req_item = ReqItem.objects.create(order=order, good=good, req_domain=goods[0], item_fam=goods[1], item_subfam=goods[2], item_details=item_details)
        req_item.req_item_created_by = user
        req_item.save()
        for k, v in validated_data['prod_details'].iteritems():
            req_product = ReqProduct(req_item=req_item, prod_fam=goods[1], prod_subfam=goods[2], prod_title=k, prod_details=v)
            req_product.save()
        log(
            user=user,
            company=order.order_company,
            not_action='request item created',
            obj=order,
            notification=False,
            extra={
                'order_id':order.id,
                'order_number':order.order_number,
                'order_version':order.order_version,
                'request_item_id':req_item.id,
                'request_item_subfam':req_item.item_subfam,
                'order_status':order.order_status,
                'order_status_full':order.get_order_status_display(),
            }
        )
        return req_item

    def update(self, instance, validated_data):
        val_data = validated_data.pop('data')
        user = validated_data['user']  
        order = validated_data.pop('order')
        order.order_draft = val_data['order_draft'] 
        order.order_modified_by = user
        order.save()
        instance.req_item_modified_by = user
        instance.item_details = val_data.get('item_details', instance.item_details) 
        for item in val_data['req_product']:
            req_product = ReqProduct(id=item['id'], prod_title=item['prod_title'], prod_details=item['prod_details'], req_item=instance)
            req_product.save()
        instance.save()
        log(
            user=user,
            company=order.order_company,
            not_action='request item updated',
            obj=order,
            notification=False,
            extra={
                'order_id':order.id,
                'order_number':order.order_number,
                'order_version':order.order_version,
                'request_item_id':instance.id,
                'request_item_subfam':instance.item_subfam,
                'order_status':order.order_status,
                'order_status_full':order.get_order_status_display(),
            }
        )
        return instance


class OrderSimpleSerializer(serializers.ModelSerializer):
    req_order = serializers.SlugRelatedField(many=True, read_only=True, slug_field='req_domain')
    offer_order = serializers.SlugRelatedField(many=True, read_only=True, slug_field='offer_domain')
    delivery_address = serializers.CharField(source='delivery_address.addr_location', required=False, read_only=True)
    order_created_date = serializers.DateTimeField(required=False)
    order_created_by_username = serializers.CharField(source='order_created_by.username', required=False)    
    order_created_by_first_name = serializers.CharField(source='order_created_by.first_name', required=False)
    order_created_by_last_name = serializers.CharField(source='order_created_by.last_name', required=False)
    order_status_change_date = serializers.DateTimeField(required=False)
    order_status_change_by_username = serializers.CharField(source='order_status_change_by.username', required=False)
    order_status_change_by_first_name = serializers.CharField(source='order_status_change_by.first_name', required=False)
    order_status_change_by_last_name = serializers.CharField(source='order_status_change_by.last_name', required=False)
    order_status_display = serializers.CharField(source='get_order_status_display', required=False)    

    class Meta:
        model = Order
        fields = ('id', 'req_order','order_company', 'order_number', 'order_version','reference_number', 'delivery_address', 'order_created', 'order_created_date', 'order_created_by', 'order_created_by_username', 'order_created_by_first_name', 'order_created_by_last_name', 'order_status',
            'order_status_display', 'order_status_change_by', 'order_status_change_by_username', 'order_status_change_by_first_name', 'order_status_change_by_last_name', 'order_status_change_date','req_order', 'offer_order', 'order_comment',)
        read_only_fields = ('order_created', 'order_status_change_by',)


class OrderSerializer(serializers.ModelSerializer):
    order_company = CompanySerializer(read_only=True)
    order_created_by = UserCompanySerializer(read_only=True, required=False)
    company_approval_by = UserCompanySerializer(read_only=True, required=False)
    delivery_address = AddressSerializer(required=False, read_only=True)
    req_order = ReqItemSerializer(many=True, read_only=False, required=False)
    offer_order = OfferSerializer(many=True, read_only=True)
    order_comment = CommentSerializer(many=True, required=False)
    order_status_change_date = serializers.DateTimeField(required=False)
    order_status_display = serializers.CharField(source='get_order_status_display', required=False)
    company_approval_status_display = serializers.CharField(source='get_company_approval_status_display', required=False)
    optiz_status_display = serializers.CharField(source='get_optiz_status_display', required=False)

    class Meta:
        model = Order
        fields = ('id', 'order_company', 'order_draft', 'order_number', 'order_version', 'offer_version', 'order_offer', 'reference_number',
            'description', 'order_total', 'delivery_address', 'order_created', 'order_created_by', 'modified_by', 'modified_by_date', 'order_status',
            'order_status_display', 'order_status_change_by', 'order_status_change_date', 'company_approval_status', 'company_approval_status_display','company_approval_by', 'company_approval_date',
            'optiz_status', 'optiz_status_display','optiz_status_change_by', 'optiz_status_change_date', 'req_order', 'offer_order', 'order_comment',)
        read_only_fields = ('order_created', 'modified_date', 'company_approval_by', 'optiz_status_change_by', 'order_status_change_by', 'modified_by',)
    
    def update(self, instance, validated_data):
        print 'VAL DATA == %s' % validated_data
        user = validated_data.pop('user')
        if 'order_draft' in validated_data:
            if 'False' in validated_data['order_draft']:
                instance.order_draft = False
                if user.access_level >= '6':
                    instance.company_approval_status = 'PEN'
                    instance.order_status = 'PEN'
                    instance.order_status_change_by = user
                    instance.order_status_change_date = timezone.now()
                    instance.optiz_status = 'PEN'
                    instance.company_approval_by = user
                    instance.company_approval_date = timezone.now()
                    instance.order_version = instance.order_version + 01
                    log(
                        user=user,
                        company=instance.order_company,
                        not_action='request submitted',
                        obj=instance,
                        notification=True,
                        extra={
                            'order_id':instance.id,
                            'order_number':instance.order_number,
                            'order_version':instance.order_version,
                            'order_status':instance.order_status,
                            'order_status_full':instance.get_order_status_display(),
                        }
                    )
                else:
                    if instance.company_approval_status == 'APN':
                        req_not_action = 'request updated'
                    else:
                        instance.company_approval_status == 'APN'
                        instance.order_status = 'APN'
                        req_not_action = 'request created'
                    log(
                        user=user,
                        company=instance.order_company,
                        not_action=req_not_action,
                        obj=instance,
                        notification=True,
                        extra={
                            'order_id':instance.id,
                            'order_number':instance.order_number,
                            'order_version':instance.order_version,
                            'order_status':instance.order_status,
                            'order_status_full':instance.get_order_status_display(),
                        }
                    )
        if 'order_status' in validated_data:
            if not validated_data['order_status'] in instance.order_status:
                instance.order_status = validated_data['order_status']
                instance.order_status_change_by = user
                instance.order_status_change_date = timezone.now()
                if not instance.order_draft:
                    order_status_full = instance.get_order_status_display()
                    print "Ord Stat F --- %s" % order_status_full
                    log(
                        user=user,
                        company=instance.order_company,
                        not_action='order status updated',
                        obj=instance,
                        notification=True,
                        extra={
                            'order_id':instance.id,
                            'order_number':instance.order_number,
                            'order_version':instance.order_version,
                            'order_status':instance.order_status,
                            'order_status_full':order_status_full,
                        }
                    )
                if 'optiz_status' in validated_data:
                    instance.optiz_status = validated_data['optiz_status']
                    instance.optiz_status_change_by = user
                    instance.optiz_status_change_date = timezone.now()
                else: 
                    instance.company_approval_status = validated_data['company_approval_status']
                    instance.company_approval_by = user
                    instance.company_approval_date = timezone.now()

                if validated_data['order_status'] == 'APV' or validated_data['order_status'] == 'REF':
                    offer = Offer.objects.get(id=validated_data['offer'])
                    offer.offer_approval_status = validated_data['order_status']
                    offer.offer_approval_by = user
                    offer.offer_approval = timezone.now()
                    offer.save()

        if 'delivery_address' in validated_data:
            addr = Address.objects.get(id=validated_data['delivery_address'])
            instance.delivery_address = addr
            log(
                user=user,
                company=instance.order_company,
                not_action='order delivery address',
                obj=instance,
                notification=False,
                extra={
                    'order_id':instance.id,
                    'order_number':instance.order_number,
                    'order_version':instance.order_version,
                    'order_delivery_address':instance.delivery_address.addr_location,
                }
            )
        if 'comment_body' in validated_data:
            comment = Comment.objects.create(order=instance, created_by=user, body=validated_data['comment_body'])
            comment.save()
            log(
                user=user,
                company=instance.order_company,
                not_action='comment added',
                obj=instance,
                notification=True,
                extra={
                    'order_id':instance.id,
                    'order_number':instance.order_number,
                    'order_version':instance.order_version,
                    'order_status':instance.order_status,
                    'order_status_full':instance.get_order_status_display(),
                    'comment':comment.body,
                }
            )
        instance.reference_number = validated_data.get('reference_number', instance.reference_number)        
        instance.modified_by = user
        instance.save()

        return instance


class DetailSerializer(serializers.ModelSerializer):
    good = serializers.CharField()

    class Meta:
        model = Detail
        fields = ('id', 'good', 'good_info', 'good_description',)


class GoodSerializer(serializers.ModelSerializer):
    good_detail = DetailSerializer(many=True)

    class Meta:
        model = Good
        fields = ('id', 'domain', 'family', 'subfamily', 'good_detail', )