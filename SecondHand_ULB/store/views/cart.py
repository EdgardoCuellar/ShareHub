from django.shortcuts import render , redirect

from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import  View
from store.models.product import Products

class Cart(View):
    def get(self , request):
        if request.session.get('cart'):
            ids = request.session.get('cart')
            products = Products.get_products_by_id(ids)
        else:
            products = []

        return render(request , 'cart.html' , {'products' : products} )

    def post(self , request):
        product_id = int(request.POST.get('product'))

        cart = request.session.get('cart')
        cart.remove(product_id)
        request.session['cart'] = cart

        ids = request.session.get('cart')
        products = Products.get_products_by_id(ids)

        return render(request , 'cart.html' , {'products' : products} )