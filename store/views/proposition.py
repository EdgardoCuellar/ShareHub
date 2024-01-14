from django.shortcuts import render , redirect

from store.models.prices import Prices
from django.views import  View
from store.models.product import Products

class PropositionView(View):
    html_template = "proposition.html"

    def get(self , request):
        if not request.session.get('customer'):
            return redirect('login')
        offers = Prices.get_prices_by_buyer_id(request.session.get('customer'))
        print("offres: ", offers)
        return render(request , self.html_template , {'offers' : offers} )

    def post(self , request):
        if not request.session.get('customer'):
            return redirect('login')
        offer_id = int(request.POST.get('offer'))
        offer = Prices.get_price_by_id(offer_id)
        offer.status = 1
        offer.save()
        
        offers = Prices.get_prices_by_buyer_id(request.session.get('customer'))
        return render(request , self.html_template , {'offers' : offers} )