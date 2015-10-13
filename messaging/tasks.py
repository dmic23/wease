from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def user_email(user, obj, subj, tmp):

    from_email = 'weasereg@gmail.com'
    to = [user.email]
    subject = subj

    html_content = render_to_string(tmp, {'user':user, 'obj':obj})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, fromg_email, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# #from django.conf import settings
# from django.contrib.auth.forms import PasswordResetForm
# from django.core.mail import EmailMessage
# from django.template import RequestContext, Context
# from django.template.loader import render_to_string, get_template
# from celery import Celery

# app = Celery('tasks', broker='redis://localhost:6379/0')

# @app.task
# def user_email(user, obj, subj, tmp):
#     ctx = {
#         'user': user,
#         'obj':obj,
#     }
#     from_email = 'weasereg@gmail.com'
#     to = [user.email]
#     subject = subj
#     message = get_template(tmp).render(Context(ctx))
#     msg = EmailMessage(subject, message, from_email, to)
#     msg.content_subtype = 'html'
#     msg.send()


@app.task
def registration_email(email, from_email, template='registration/password_reset_email_reg.html'):

    form = PasswordResetForm({'email': email})
    if form.is_valid():
        subject='registration/password_reset_email_reg.txt'
        return form.save(subject_template_name=subject, from_email=from_email, html_email_template_name=template)






