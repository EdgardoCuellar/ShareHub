from django.shortcuts import render , redirect

from store.models.product import Products
from store.models.category import Category
from django.views import  View

class Product(View):
    def get(self , request, product_id=None):
        if product_id is not None and Products.product_exists(product_id):
            product = Products.get_product_by_id(product_id)
            category = product.category
            return render(request , 'product.html' , {'product' : product, 'category': category} )
        else:
            return redirect('homepage')
