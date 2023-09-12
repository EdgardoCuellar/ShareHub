from django.shortcuts import render , redirect

from store.models.product import Products
from store.models.category import Category
from django.views import  View

class Product(View):
    def get(self , request, product_id=None):
        if product_id is not None and Products.product_exists(product_id):
            product = Products.get_product_by_id(product_id)
            category = product.category
            product_in_cart = False
            
            if product_id in request.session['cart']:
                product_in_cart = True
            
            return render(request , 'product.html' , {'product' : product, 'category': category, 'product_in_cart': product_in_cart} )
        else:
            return redirect('store')

    def post(self , request, product_id=None):
        product = Products.get_product_by_id(product_id)
        category = product.category
        cart = request.session.get('cart')
        product_in_cart = True
        if not cart:
            cart = []
        if product_id in cart:
            product_in_cart = False
            cart.remove(product_id)
        else:
            cart.append(product_id)
        request.session['cart'] = cart

        return render(request , 'product.html' , {'product' : product, 'category': category, 'product_in_cart': product_in_cart} )