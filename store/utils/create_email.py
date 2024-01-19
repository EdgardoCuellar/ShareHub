from store.models.customer import Customer
from store.models.product import Products
from store.models.forgot_password import ForgotPassword

import os
from django.conf import settings


def create_email_buy(request, product: Products):
    html_file_path = os.path.join(settings.BASE_DIR, 'static', 'mails', 'buy.html')
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    html_content = html_content.replace('#name#', product.name)
    html_content = html_content.replace("#link#", request.META['HTTP_HOST'])

    return html_content


def create_email_sell(request, product: Products):
    html_file_path = os.path.join(settings.BASE_DIR, 'static', 'mails', 'buy.html')
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    html_content = html_content.replace('#name#', product.name)
    html_content = html_content.replace("#link#", request.META['HTTP_HOST'])

    return html_content
    
def create_forgot_password(request, forgot_password: ForgotPassword):
    html_file_path = os.path.join(settings.BASE_DIR, 'static', 'mails', 'forgot_password.html')
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    html_content = html_content.replace('#token#', forgot_password.token)
    html_content = html_content.replace('#get_host#', request.META['HTTP_HOST'])

    return html_content
