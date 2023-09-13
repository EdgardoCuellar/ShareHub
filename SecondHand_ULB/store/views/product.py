from django.shortcuts import render , redirect

from store.models.product import Products
from store.models.category import Category
from store.models.rating import Rating
from django.views import  View

class Product(View):
    def get(self , request, product_id=None):
        if product_id is not None and Products.product_exists(product_id):
            product = Products.get_product_by_id(product_id)
            category = product.category
            product_in_cart = False
            
            rating = Rating.get_rating(product.user_id)

            if product_id in request.session['cart']:
                product_in_cart = True
            
            return render(request , 'product.html' , {'product' : product, 'category': category, 'product_in_cart': product_in_cart, 'rating': rating} )
        else:
            return redirect('store')

    def post(self , request, product_id=None):
        product = Products.get_product_by_id(product_id)
        category = product.category
        cart = request.session.get('cart')
        rating = Rating.get_rating(product.user_id)
        
        product_in_cart = True
        if not cart:
            cart = []
        if product_id in cart:
            product_in_cart = False
            cart.remove(product_id)
        else:
            cart.append(product_id)
        request.session['cart'] = cart

        return render(request , 'product.html' , {'product' : product, 'category': category, 'product_in_cart': product_in_cart, 'rating': rating} )

def remove(request, product_id):
    if request.session.get('customer') != Products.get_product_by_id(product_id).user_id:
        return redirect('store')
    Products.remove_product_by_id(product_id)
    return redirect('store')