from django import template
from store.models.customer import Customer

register = template.Library()

@register.filter(name='currency')
def currency(number):
    price = number / 100
    return str(price) + " €"

@register.filter(name='min_price')
def min_price(price):
    price = price - int(price * 0.2)  
    return price

@register.filter(name='user_name')
def get_user_name(id):
    return Customer.get_customer_by_id(id).first_name

@register.filter(name='user_img')
def get_user_img(id):
    return f"/media/img/user_{id % 11}.png"
