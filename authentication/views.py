# -*- coding: utf-8 -*-
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import RequestContext, Context
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response
# from authentication.permissions import IsAccountOwner
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
            user = self.request.user
            user_company = Company.objects.get(id=self.request.data['company'])
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
            registration_email(acct.email, 'weasereg@gmail.com')
            for uc in user_company.wease_company.all():
                if uc.id != acct.id and uc.new_user_email:
                    print "UC ____ %s" % uc
                    user_email(uc, acct, subj='New WeASe member added', tmp='registration/user_added_email.html')
            for optiz in user_company.company_assigned_to.all():
                if optiz.new_user_email:
                    print "OP ____ %s" % optiz
                    user_email(optiz, acct, subj='New WeASe member added', tmp='registration/user_added_email.html')
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


def registration_email(email, from_email, template='registration/password_reset_email_reg.html'):

    form = PasswordResetForm({'email': email})
    if form.is_valid():
        subject='registration/password_reset_email_reg.txt'
        return form.save(subject_template_name=subject, from_email=from_email, html_email_template_name=template)

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

def user_email(user, obj, subj, tmp):
    ctx = {
        'user': user,
        'obj':obj,
    }
    from_email = 'weasereg@gmail.com'
    to = [user.email]
    subject = subj
    message = get_template(tmp).render(Context(ctx))
    msg = EmailMessage(subject, message, from_email, to)
    msg.content_subtype = 'html'
    msg.send()
