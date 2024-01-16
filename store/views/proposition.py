from django.shortcuts import render , redirect

from store.models.prices import Prices
from django.views import  View
from store.models.product import Products

from django.utils.decorators import method_decorator
from store.utils.decorators import user_login_required

class PropositionView(View):
    html_template = "proposition.html"

    @method_decorator(user_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self , request):
        offers = Prices.get_prices_by_buyer_id(request.session.get('customer'))
        return render(request , self.html_template , {'offers' : offers} )

    def post(self , request):
        offer_id = int(request.POST.get('offer'))
        offer = Prices.get_price_by_id(offer_id)
        offer.status = 1
        offer.save()
        
        offers = Prices.get_prices_by_buyer_id(request.session.get('customer'))
        return render(request , self.html_template , {'offers' : offers} )