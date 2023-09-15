from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View

from store.models.product import Products
from store.models.orders import Order


class CheckOut(View):
    def post(self, request):
        buyer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(cart)

        for product in products:
            order = Order(buyer=Customer(id=buyer),
                          seller=Customer(id=product.user_id),
                          product=Products(id=product.id),
                          price=product.price,
                          status=False,)
            order.save()
            product.sold = True
            product.save()


        request.session['cart'] = {}

        return redirect('cart')
