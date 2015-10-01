# -*- coding: utf-8 -*-
import json
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response
# from authentication.permissions import IsAccountOwner
from django.utils import timezone
from ipware.ip import get_ip
from eventlog.models import log
from authentication.models import Account, Company, Address
from authentication.serializers import AccountSerializer, CompanySerializer, AddressSerializer, UserCompanySerializer

class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        if serializer.is_valid():
            print "ser --- %s" % serializer.data
            print "SRD --- %s" % self.request.data['company']
            user = self.request.user
            user_company = Company.objects.get(id=self.request.data['company'])
            print "COMPANY ==== %s" % user_company
            acct = Account.objects.create_user(**serializer.validated_data)
            acct.user_company = user_company
            acct.user_created_by = user
            acct.access_level = serializer.data['access_level']
            acct.position = serializer.data['position']
            acct.auth_amount = serializer.data['auth_amount']
            acct.save()
            log(
                user=user,
                company=user_company,
                not_action='user created',
                obj=acct,
                notification=True,
                extra={
                    'account_id':acct.id,
                    'account_username':acct.username,
                    'account_first_name':acct.first_name,
                    'account_last_name':acct.last_name,
                }
            )
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        if serializer.is_valid():
            if 'file' in self.request.data:
                user_pic = self.request.data['file']
                serializer.save(user=self.request.user, user_pic=user_pic, **self.request.data)
            else:
                serializer.save(user=self.request.user, **self.request.data)

class CompanyViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            serializer.save(user=user, **self.request.data)

        #     return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        # return Response({
        #     'status': 'Bad request',
        #     'message': 'Company could not be created with received data.'
        # }, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        if serializer.is_valid():
            if 'file' in self.request.data:
                company_logo = self.request.data['file']
                print "COMP LOGO == %s" % company_logo
                serializer.save(user=self.request.user, company_logo=company_logo, **self.request.data)
            else:    
                serializer.save(user=self.request.user, **self.request.data)

class AddressViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user, **self.request.data)

class OptizViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Account.objects.filter(optiz=True)
    serializer_class = UserCompanySerializer


class LoginView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)

        email = data.get('email', None)
        password = data.get('password', None)

        account = authenticate(email=email, password=password)
        print "ACCT -- %s" %account
        if account is not None:
            if account.is_active:
                login(request, account)
                serialized = AccountSerializer(account)
                user = self.request.user
                ip = get_ip(request)
                log(
                    user=user,
                    company=user.user_company,
                    not_action='user login',
                    obj=user,
                    notification=False,
                    extra={
                        'account_id':user.id,
                        'account_first_name':user.first_name,
                        'account_last_name':user.last_name,
                        'login_ip':ip,
                    }
                )
                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username or password invalid'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user
        print "USER LOGOUT --- %s"%user
        ip = get_ip(request)
        log(
            user=user,
            company=user.user_company,
            not_action='user logout',
            obj=user,
            notification=False,
            extra={
                'account_id':user.id,
                'account_first_name':user.first_name,
                'account_last_name':user.last_name,
                'login_ip':ip,
            }
        )
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
