from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.middlewares.auth import auth_middleware

class MyProductsView(View):

    html_template = "products/my_products.html"

    def get(self , request ):
        if not request.session.get('customer'):
            return redirect('login')

        customer = request.session.get('customer')
        products = Products.get_products_by_userid(customer)
        
        return render(request , self.html_template  , {'products' : products})




