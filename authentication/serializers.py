# -*- coding: utf-8 -*-
from django.contrib.auth import update_session_auth_hash
from django.forms import widgets
from rest_framework import serializers
from eventlog.models import log
from authentication.models import Account, Company, Address


class UserCompanySerializer(serializers.ModelSerializer):
    user_pic = serializers.CharField(read_only=True)
    user_name_full = serializers.CharField(source='get_full_name', required=False)
    user_company_full = serializers.CharField(source='user_company', required=False)
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'user_name_full', 'first_name', 'last_name', 'optiz', 'lang', 
                'user_company', 'user_company_full', 'position', 'access_level', 'auth_amount', 'street_addr1',
                'street_addr2', 'city', 'post_code', 'country', 'phone_main', 'phone_mobile', 'user_pic',)


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'addr_type', 'addr_location', 'addr_company', 'addr_user', 'street_addr1', 'street_addr2', 'city',
            'post_code', 'country', 'phone_main', 'email', 'addr_notes',)

    def create(self, validated_data):
        print "VAL-DATA ADDR === %s" % validated_data
        user = validated_data.pop('user')
        if 'addr_company' in validated_data:
            addr_comp = validated_data.pop('addr_company')
            print "ADDR COMP -- %s" % addr_comp
            comp = Company.objects.get(id=addr_comp)
        else:
            addr_user = Account.objects.get(id=validated_data['addr_user'])
            comp = addr_user.user_company
        new_addr = Address.objects.create(addr_created_by=user, addr_company=comp, **validated_data)
        new_addr.save()
        log(
            user=user,
            company=comp,
            not_action='address created',
            obj=new_addr,
            notification=False,
            extra={
                'address_id':new_addr.id,
                'company_name':new_addr.addr_location,
            }
        )
        return new_addr


class CompanySerializer(serializers.ModelSerializer):
    wease_company = UserCompanySerializer(many=True, required=False)
    company_assigned_to = UserCompanySerializer(many=True, required=False)
    address_company = AddressSerializer(many=True, read_only=True)  
    company_address = AddressSerializer(required=False)    
    company_created_by = serializers.CharField(read_only=True)
    company_updated_by = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True, required=False)
    company_logo = serializers.CharField(read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'company_logo', 'company_created', 'email', 'company_created_by', 'company_updated', 'company_updated_by', 'company_assigned_to','address_company',
            'company_address', 'company_website', 'wease_company',)
        read_only_fields = ('company_updated', 'company_created',)

    def create(self, validated_data):
        print "VAL-DATA COMP === %s" % validated_data
        user = validated_data.pop('user')
        addr = validated_data.pop('company_address')
        comp_assign = validated_data.pop('assign_optiz')
        print "assign_optiz === %s" % comp_assign
        comp = Company.objects.create(company_created_by=user, **validated_data)
        for optiz in comp_assign:
            optiz_user = Account.objects.get(id=optiz)
            comp.company_assigned_to.add(optiz_user)
        comp.save()
        comp_addr = Address.objects.create(addr_created_by=user, addr_company=comp, **addr)
        comp_addr.save()
        comp.company_address = comp_addr
        comp.save()
        log(
            user=user,
            company=comp,
            not_action='company registered',
            obj=comp,
            notification=True,
            extra={
                'company_id':comp.id,
                'company_name':comp.name,
            }
        )
        return comp

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        if 'default_address' in validated_data:
            def_addr = validated_data.pop('default_address')
            comp_addr = Address.objects.get(id=def_addr['id'])
            instance.company_address = comp_addr
        elif 'company_address' in validated_data:
            company_address = validated_data.pop('company_address')
            if 'id' in company_address:
                comp_addr = Address.objects.get(id=company_address['id'])
                comp_addr.street_addr1 = company_address.get('street_addr1', comp_addr.street_addr1)
                comp_addr.street_addr2 = company_address.get('street_addr2', comp_addr.street_addr2)
                comp_addr.city = company_address.get('city', comp_addr.city)
                comp_addr.post_code = company_address.get('post_code', comp_addr.post_code)
                comp_addr.country = company_address.get('country', comp_addr.country)
                comp_addr.email = company_address.get('email', comp_addr.email)
                comp_addr.phone_main = company_address.get('phone_main', comp_addr.phone_main)
                comp_addr.addr_notes = company_address.get('addr_notes', comp_addr.addr_notes)
                comp_addr.addr_location = company_address.get('addr_location', comp_addr.addr_location)
                comp_addr.save()
        if 'assign_optiz' in validated_data:
            opt_users = validated_data['assign_optiz']
            for ou in instance.company_assigned_to.all():
                if not ou.id in opt_users:
                    instance.company_assigned_to.remove(ou)
            for optiz in opt_users:
                if not instance.company_assigned_to.all().filter(id=optiz).exists():
                    optiz_user = Account.objects.get(id=optiz)
                    print "OPTIZ ASS === %s" % optiz_user
                    instance.company_assigned_to.add(optiz_user)
                    log(
                        user=user,
                        company=instance,
                        not_action='optiz assigned',
                        obj=instance,
                        notification=True,
                        extra={
                            'company_id':instance.id,
                            'company_name':instance.name,
                            'optiz_assigned':optiz_user.username,
                            'optiz_assigned_name': ''.join([str(optiz_user.first_name),' ',str(optiz_user.last_name)])
                        }
                    )
        else:
            log(
                user=user,
                company=instance,
                not_action='company updated',
                obj=instance,
                notification=True,
                extra={
                    'company_id':instance.id,
                    'company_name':instance.name,
                }
            )            
        instance.name = validated_data.get('name', instance.name)
        instance.company_website = validated_data.get('company_website', instance.company_website)
        instance.company_logo = validated_data.get('company_logo', instance.company_logo)
        instance.company_updated_by = user
        instance.save()

        return instance


class AccountSerializer(serializers.ModelSerializer):
    user_company_full = serializers.CharField(source='user_company.get_name', read_only=True, required=False)
    user_company = serializers.CharField(source='user_company.id',required=False)
    username = serializers.CharField(required=False)
    user_name_full = serializers.CharField(source='get_full_name', required=False)
    email = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    user_created_by = serializers.CharField(read_only=True)
    user_updated_by = serializers.CharField(read_only=True)
    user_pic = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'user_name_full', 'user_created', 'user_created_by', 'user_updated', 'user_updated_by',
                  'first_name', 'last_name', 'password','confirm_password', 'optiz', 'lang', 'user_company', 'user_company_full',
                  'position', 'access_level', 'auth_amount', 'street_addr1', 'street_addr2', 'city', 'post_code', 'country',
                  'phone_main', 'phone_mobile', 'user_pic', 'request_email', 'refused_email', 'offer_email', 'order_email',
                  'approval_email', 'validated_email', 'canceled_email', 'new_user_email', 'info_change_email', 'tagline',)

        read_only_fields = ('user_created', 'user_company', 'user_updated',)

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print "SELF === %s" % self
        print "INST === %s" % instance
        print "VAL-DATA === %s" % validated_data
        user = validated_data.pop('user')
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.tagline = validated_data.get('tagline', instance.tagline)       
        instance.optiz = validated_data.get('optiz', instance.optiz)
        instance.lang = validated_data.get('lang', instance.lang)
        instance.position = validated_data.get('position', instance.position)
        instance.access_level = validated_data.get('access_level', instance.access_level)
        instance.auth_amount = validated_data.get('auth_amount', instance.auth_amount)
        instance.street_addr1 = validated_data.get('street_addr1', instance.street_addr1)
        instance.street_addr2 = validated_data.get('street_addr2', instance.street_addr2)
        instance.city = validated_data.get('city', instance.city)
        instance.post_code = validated_data.get('post_code', instance.post_code)
        instance.country = validated_data.get('country', instance.country)
        instance.phone_main = validated_data.get('phone_main', instance.phone_main)
        instance.phone_mobile = validated_data.get('phone_mobile', instance.phone_mobile)
        instance.user_pic = validated_data.get('user_pic', instance.user_pic)
        instance.request_email = validated_data.get('request_email', instance.request_email)
        instance.refused_email = validated_data.get('refused_email', instance.refused_email)
        instance.offer_email = validated_data.get('offer_email', instance.offer_email)
        instance.order_email = validated_data.get('order_email', instance.order_email)
        instance.approval_email = validated_data.get('approval_email', instance.approval_email)
        instance.validated_email = validated_data.get('validated_email', instance.validated_email)
        instance.canceled_email = validated_data.get('canceled_email', instance.canceled_email)
        instance.new_user_email = validated_data.get('new_user_email', instance.new_user_email)
        instance.info_change_email = validated_data.get('info_change_email', instance.info_change_email)
        instance.user_updated_by = user
        instance.save()
        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.save()

            update_session_auth_hash(self.context.get('request'), instance)
        log(
            user=user,
            company=instance.user_company,
            not_action='user updated',
            obj=instance,
            notification=False,
            extra={
                'account_id':instance.id,
                'account_first_name':instance.first_name,
                'account_last_name':instance.last_name,
            }
        )
        return instance