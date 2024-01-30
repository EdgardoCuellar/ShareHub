from django.shortcuts import render , redirect

from store.models.prices import Prices
from store.models.product import Products

from django.views import  View

from django.utils.decorators import method_decorator
from store.utils.decorators import user_login_required

class Overview(View):

    @method_decorator(user_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self , request, product_id, offer_id):
        product = Products.get_product_by_id(product_id)
        offer = Prices.get_price_by_id(offer_id)
        if not product:
            return redirect('index')
        if not offer:
            return redirect('index')
        return render(request , 'overview.html' , {'product' : product, 'offer': offer} )