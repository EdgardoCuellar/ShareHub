from django.shortcuts import render , redirect

from store.models.prices import Prices
from django.views import  View
from store.models.product import Products

class Cart(View):
    def get(self , request):
        if not request.session.get('customer'):
            return redirect('login')
        offers = Prices.get_prices_by_buyer_id(request.session.get('customer'))
        print("offres: ", offers)
        return render(request , 'cart.html' , {'offers' : offers} )

    def post(self , request):
        if not request.session.get('customer'):
            return redirect('login')
        offer_id = int(request.POST.get('product'))
        offer = Prices.get_price_by_id(offer_id)
        offer.delete()
        
        offers = Prices.get_prices_by_buyer_id(request.session.get('customer'))
        return render(request , 'cart.html' , {'offers' : offers} )