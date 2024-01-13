from django import template

register = template.Library ()


@register.filter (name='total_cart_price')
def total_cart_price(products):
    sum = 0;
    for p in products:
        sum += p.price

    return sum
