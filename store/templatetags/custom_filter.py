from django import template
from store.models.customer import Customer
from store.models.product import Products
from store.models.product_img import ProductImage

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