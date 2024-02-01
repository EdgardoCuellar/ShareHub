from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from anymail.message import attach_inline_image_file
import requests
from tempfile import NamedTemporaryFile

from store.models.customer import Customer as User
from store.models.product import Products
from store.models.forgot_password import ForgotPassword

from .create_email import create_email_sell, create_email_buy, create_forgot_password

from django.core.mail import EmailMultiAlternatives, send_mail

def send_mail_sell(request, product: Products, user: User):
        
    subject = "ShareHub - vente conclue"
    message = create_email_sell(request, product)
    from_email = "no-reply@sharehub.social"
    recipient_list = [user.email]  

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def send_mail_buy(request, product: Products, user: User):
        
    subject = "ShareHub - offre acceptée"
    message = create_email_buy(request, product)
    from_email = "no-reply@sharehub.social"
    recipient_list = [user.email]  

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def send_reset_password(request, forget_password: ForgotPassword):
        
    subject = "Réinitialiser votre mot de passe Rentizy"
    message = create_forgot_password(request, forget_password)
    from_email = "no-reply@sharehub.social"
    recipient_list = [forget_password.customer.email]  

    email = EmailMultiAlternatives(
        subject=subject,
        body="ShareHub",
        from_email=from_email,
        to=recipient_list,
    )

    # Now you can use the path of img_temp in attach_inline_image_file
    email.attach_alternative(message, "text/html")

    email.send()

    # send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    # send_mail(
    #     'Réinitialiser votre mot de passe Rentizy',
    #     "ShareHub",
    #     settings.DEFAULT_FROM_EMAIL,
    #     [forget_password.customer.email],
    #     fail_silently=False,
    #     html_message=create_forgot_password(request, forget_password),
    # )

    # return requests.post(
    #     "https://api.eu.mailgun.net/v3/sharehub.social/messages",
    #     auth=("api", "a77af78f57cbf370c9401f73d8c5620d-69a6bd85-9a03c1e5"),
    #     data={"from": "no-reply@sharehub.social",
    #         "to":forget_password.customer.email,
    #         "subject": "Réinitialiser votre mot de passe Rentizy",
    #         "template": "Forgot password",
    #         "h:X-Mailgun-Variables": {'token': forgot_password.token}})
