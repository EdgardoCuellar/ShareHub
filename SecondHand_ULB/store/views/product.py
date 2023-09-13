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
            
            rating = self.get_user_rating(product.user_id)

            if product_id in request.session['cart']:
                product_in_cart = True
            
            return render(request , 'product.html' , {'product' : product, 'category': category, 'product_in_cart': product_in_cart, 'rating': rating} )
        else:
            return redirect('store')

    def post(self , request, product_id=None):
        product = Products.get_product_by_id(product_id)
        category = product.category
        cart = request.session.get('cart')
        rating = self.get_user_rating(product.user_id)
        
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

    def get_user_rating(self, user_id):
        sell_count = Rating.get_count_user_sells(user_id)
        user_rating = Rating.get_user_rating(user_id)
        rating = {
            'sell_count': sell_count,
            'user_rating': user_rating
        }

        return rating