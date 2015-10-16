# -*- coding: utf-8 -*-
from django.contrib.auth.forms import PasswordResetForm
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import Celery
from io import BytesIO
from wease.printing import MyPrint 



app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def user_email(user, obj, subj, tmp):
    print "Here Tasks!"
    from_email = 'weasereg@gmail.com'
    to = [user.email]
    subject = subj

    html_content = render_to_string(tmp, {'user':user, 'obj':obj})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, 'text/html')
    print "OBJECT  ---- %s" %obj
    if obj.order_number:
        pdf_name = ''.join([str(obj.order_number),"/v",str(obj.order_version),".pdf"])
        pdf = create_pdf(obj, pdf_name)
    msg.attach(pdf_name, pdf, 'application/pdf')
    msg.send()


@app.task
def registration_email(email, from_email, template='registration/password_reset_email_reg.html'):

    form = PasswordResetForm({'email': email})
    if form.is_valid():
        subject='registration/password_reset_email_reg.txt'
        return form.save(subject_template_name=subject, from_email=from_email, html_email_template_name=template)


def create_pdf(obj, pdf_name):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
 
    buffer = BytesIO()
 
    report = MyPrint(buffer, 'A4')
    pdf = report.build_pdf(obj)
    new_pdf = ContentFile(pdf)
    # req_item = ReqItem.objects.get(id=4)
    # pdf_order = ReqFile.objects.create(req_item=req_item)
    # pdf_order.req_file.save(pdf_name,new_pdf)
    response.write(pdf)
    return pdf

@app.task
def mail_item(user, obj, subj, tmp):
    #user_email.delay(user, order, subj='offer', tmp='registration/order_confirm_email.html')
    for uc in obj.order_company.wease_company.all():
        if obj.order_status in ['WRQ', 'PEN']:
            if uc.request_email:
                if uc.access_level >= 5 and uc.approval_email:
                    template = 'registration/approval_email.html'
                    user_email(uc, obj, subj, template)
                else:
                    user_email(uc, obj, subj, tmp)
        if obj.order_status in ['OFR', 'REF', 'APV']:
            if uc.offer_email or uc.validated_email or uc.refused_email:
                if uc.access_level >= 5 and uc.approval_email:
                    template = 'registration/approval_email.html'
                    user_email(uc, obj, subj, template)
                else:
                    user_email(uc, obj, subj, tmp)
        if obj.order_status in ['COM', 'INV', 'CAN', 'ARC']:
            if uc.order_email or uc.canceled_email or uc.validated_email or uc.refused_email:
                user_email(uc, obj, subj, tmp)
    for optiz in obj.order_company.company_assigned_to.all():
        if obj.order_status in ['PEN']:
            if optiz.approval_email or optiz.request_email:
                user_email(optiz, obj, subj, tmp)
        if obj.order_status in ['OFR', 'REF', 'APV']:
            if optiz.approval_email or optiz.offer_email or optiz.validated_email or optiz.refused_email:
                user_email(optiz, obj, subj, tmp)
        if obj.order_status in ['COM', 'INV', 'CAN', 'ARC']:
            if optiz.order_email or optiz.canceled_email or optiz.validated_email or optiz.refused_email:
                user_email(optiz, obj, subj, tmp)


