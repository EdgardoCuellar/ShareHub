from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from store.models.customer import Customer as User
from store.models.product import Products
from store.models.forgot_password import ForgotPassword

from .create_email import create_email_sell, create_email_buy, create_forgot_password


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

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
