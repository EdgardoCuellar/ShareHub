from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.models.orders import Order
from store.middlewares.auth import auth_middleware

class Sales(View):


    def get(self , request ):
        if not request.session.get('customer'):
            return redirect('login')

        seller = request.session.get('customer')
        orders = Order.get_orders_by_seller(seller)
        
        return render(request , 'sales.html'  , {'orders' : orders})
