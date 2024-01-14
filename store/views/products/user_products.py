from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.middlewares.auth import auth_middleware

class UserProductsView(View):

    html_template = "products/user_products.html"

    def get(self , request, customer_id=None):
        if customer_id is None:
            return redirect('index')
        
        customer = Customer.get_customer_by_id(customer_id)
        products = Products.get_products_by_userid(customer)
        
        return render(request , self.html_template  , {'user': customer, 'products' : products})




