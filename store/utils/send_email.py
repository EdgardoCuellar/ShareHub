from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from anymail.message import attach_inline_image_file

from store.models.customer import Customer as User
from store.models.product import Products
from store.models.forgot_password import ForgotPassword

from .create_email import create_email_sell, create_email_buy, create_forgot_password

from django.core.mail import EmailMultiAlternatives, send_mail

def send_mail_sell(request, product: Products, user: User):
        
    subject = "ShareHub - vente conclue"
    message = create_email_sell(request, product)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]  

    email = EmailMultiAlternatives(
        subject=subject,
        body="ShareHub",
        from_email=from_email,
        to=recipient_list,
    )

    email.attach_alternative(message, "text/html")

    email.send()

def send_mail_buy(request, product: Products, user: User):
        
    subject = "ShareHub - offre acceptée"
    message = create_email_buy(request, product)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]  

    email = EmailMultiAlternatives(
        subject=subject,
        body="ShareHub",
        from_email=from_email,
        to=recipient_list,
    )

    email.attach_alternative(message, "text/html")

    email.send()

def send_reset_password(request, forget_password: ForgotPassword):
        
    subject = "Réinitialiser votre mot de passe Rentizy"
    message = create_forgot_password(request, forget_password)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [forget_password.customer.email]  

    email = EmailMultiAlternatives(
        subject=subject,
        body="ShareHub",
        from_email=from_email,
        to=recipient_list,
    )

    email.attach_alternative(message, "text/html")

    email.send()
