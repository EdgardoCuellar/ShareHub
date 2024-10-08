from django import template
from store.models.customer import Customer
from store.models.product import Products
from store.models.category import Category
from store.models.prices import Prices
from store.models.product_img import ProductImage
from store.models.message import Message
from store.models.orders import Order
import time

register = template.Library()

@register.filter(name='currency')
def currency(number):
    price = number / 100
    return str(price) + " €"

@register.filter(name='min_price')
def min_price(price):
    price = price - int(price * 0.2)  
    return price

@register.filter(name='timestamp_to_date')
def timestamp_to_date(timestamp):
    return time.strftime('%d/%m/%Y', time.localtime(timestamp))

@register.filter(name='user_name')
def get_user_name(id):
    return Customer.get_customer_by_id(id).first_name

@register.filter(name='user_img')
def get_user_img(id):
    return f"img/user_{id % 11}.png"

@register.filter(name='get_first_image_product')
def get_first_image_product(product_id):
    return ProductImage.get_images_by_product_id(product_id)[0].image.url

@register.filter(name='get_all_images_product')
def get_all_images_product(product_id):
    return ProductImage.get_images_by_product_id(product_id)


@register.filter(name='get_len_images_product')
def get_all_images_product(product_id):
    nb_img = len(ProductImage.get_images_by_product_id(product_id))
    str_nb = ""
    for i in range(0, nb_img):
        str_nb += str(i)
    return str_nb

@register.filter(name='is_only_one_image')
def is_only_one_image(product_id):
    nb_img = len(ProductImage.get_images_by_product_id(product_id))
    if nb_img == 1:
        return True
    return False

@register.filter(name='get_category_name')
def get_category_name(category_id):
    return Category.get_category_by_id(category_id).name

@register.simple_tag
def define(val=None):
    return val

@register.filter(name='get_nb_offers')
def get_nb_offers(product_id):
    return len(Prices.get_prices_by_product_id(product_id))

@register.filter(name="get_nb_sells")
def get_nb_sells(user_id):
    nb = Order.get_orders_by_seller(user_id).count()
    if nb == 0:
        return ""
    else:
        return nb
    
@register.filter(name="get_nb_unseen_msg")
def get_nb_unseen_msg(user_id):
    user = Customer.get_customer_by_id(user_id)
    nb = Message.get_nb_unseen_msg(user)
    if nb == 0:
        return ""
    else:
        return nb
    
@register.filter(name="get_nb_unseen_msg_per_sender")
def get_nb_unseen_msg_per_sender(user_id, sender_id):
    user = Customer.get_customer_by_id(user_id)
    sender = Customer.get_customer_by_id(sender_id)
    nb = Message.get_nb_unseen_msg_per_sender(user=user, sender=sender)
    if nb == 0:
        return ""
    else:
        return nb

@register.filter(name="get_nb_orders")
def get_nb_orders(user_id):
    nb = Order.get_orders_by_buyer(user_id).count()
    if nb == 0:
        return ""
    else:
        return nb