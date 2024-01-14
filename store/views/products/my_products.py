from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.middlewares.auth import auth_middleware

from django.utils.decorators import method_decorator
from store.utils.decorators import user_login_required

class MyProductsView(View):

    html_template = "products/my_products.html"

    @method_decorator(user_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self , request ):
        customer = request.session.get('customer')
        products = Products.get_products_by_userid(customer)
        
        return render(request , self.html_template  , {'products' : products})




