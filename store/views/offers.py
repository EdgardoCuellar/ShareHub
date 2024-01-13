from django.shortcuts import render , redirect

from store.models.prices import Prices
from django.views import  View
from store.models.product import Products
import random

class Offers(View):
    def get(self , request):
        if not request.session.get('customer'):
            return redirect('login')            
        products_offer = self.get_offers(request)
        return render(request , 'offers.html' , {'products': products_offer} )

    def post(self , request):
        if not request.session.get('customer'):
            return redirect('login')
        offer_id = int(request.POST.get('offer'))
        offer = Prices.get_price_by_id(offer_id)
        offer.status = 1
        
        products_offer = self.get_offers(request)
        return render(request , 'offers.html' , {'products' : products_offer} )
    
    def get_offers(self, request):
        products = Products.get_products_by_userid(request.session.get('customer'))
        offers = []
        len_offers = []
        for product in products:
            temp_offers = Prices.get_prices_by_product_id(product.id)
            len_offers.append(len(temp_offers))
            # select only one offer from temp_offers randomly
            if len(temp_offers) > 0:
                offer = temp_offers[random.randint(0, len(temp_offers)-1)]
                offers.append(offer)
            else:
                offers.append(None)
                
        products_offer = []
        for i in range(len(products)):
            products_offer.append((products[i], offers[i], len_offers[i]))
        return products_offer