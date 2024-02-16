from django.shortcuts import render , redirect

from store.models.prices import Prices
from django.views import  View
from store.models.product import Products, MIN_TIME_BEFORE_ACCEPT_OFFER, MIN_TIME_BEFORE_ACCEPT_SINGLE_OFFER
from store.models.orders import Order
import random
import time

from store.utils.send_email import send_mail_sell, send_mail_buy
from store.models.message import Message
from store.models.customer import Customer

from django.utils.decorators import method_decorator
from store.utils.decorators import user_login_required

class Offers(View):

    @method_decorator(user_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self , request):
        products_offer = self.get_offers(request)
        return render(request , 'offers.html' , {'products': products_offer} )

    def post(self , request):
        product_id = request.POST.get('product_id')

        offer = self.choice_an_offer(Products.get_product_by_id(product_id))

        Prices.accept_offer_by_id(offer.id)

        order = Order(buyer=Customer(id=offer.buyer.id),
                        seller=Customer(id=offer.seller.id),
                        product=Products(id=offer.product.id),
                        price=offer.price,
                        status=False,)
        order.save()
        offer.product.sold = True
        offer.product.save()

        # Send an email to the buyer
        send_mail_buy(request, offer.product, offer.buyer)
        send_mail_sell(request, offer.product, offer.seller)

        # Send a message to the buyer
        content = "Votre offre a été acceptée pour le produit " + offer.product.name + " au prix de " + str(offer.price / 100) + "€"

        Message.send_message(sender_id=offer.seller.id,
                            receiver_id=offer.buyer.id,
                            content=content)

        return redirect('overview', product_id=product_id, offer_id=offer.id)
    
    def get_offers(self, request):
        products = Products.get_products_by_userid(request.session.get('customer'))
        offers = []
        len_offers = []
        for product in products:
            temp_offers = Prices.get_prices_by_product_id(product.id)
            len_offers.append(len(temp_offers))
            if len(temp_offers) == 0:
                offers.append("Vous n'avez pas d'offre pour ce produit")
            elif len(temp_offers) == 1:
                if temp_offers[0].timestamp - product.timestamp > MIN_TIME_BEFORE_ACCEPT_SINGLE_OFFER:
                    offers.append(None)
                else:    
                    min_day = int((MIN_TIME_BEFORE_ACCEPT_SINGLE_OFFER - (temp_offers[0].timestamp - product.timestamp)) / (60 * 60 * 24))
                    if min_day > 0:
                        offers.append("Vous ne pouvez pas accepter une seule offre avant "+ str(min_day) + " jours ou qu'une autre offre soit faite.")
                    else:
                        min_hour = int((MIN_TIME_BEFORE_ACCEPT_SINGLE_OFFER - (temp_offers[0].timestamp - product.timestamp)) / (60 * 60))
                        offers.append("Vous ne pouvez pas accepter une seule offre avant "+ str(min_hour) + " heures ou qu'une autre offre soit faite.")
            else:
                if temp_offers[0].timestamp - product.timestamp > MIN_TIME_BEFORE_ACCEPT_OFFER:
                    offers.append(None)
                else:
                    min_day = int((MIN_TIME_BEFORE_ACCEPT_OFFER - (temp_offers[0].timestamp - product.timestamp)) / (60 * 60 * 24))
                    offers.append("Vous ne pouvez pas accepter une offre avant "+ str(min_day) + " jours.")
            
        products_offer = []
        for i in range(len(products)):
            products_offer.append((products[i], offers[i], len_offers[i]))
        return products_offer

    def choice_an_offer(self, product):
        offers = Prices.get_prices_by_product_id(product.id)
        if len(offers) == 1:
            accepted_offer = Prices.accept_offer_by_id(offers[0].id)
        else:
            # get the id of the offer with the closest price to the product price, and if there are several that are less 1@ close, take the first one
            sorted_offers = sorted(offers, key=lambda offer: abs(offer.price - product.price))
            accepted_offer = sorted_offers[random.randint(0, 1)]
                
            # refuse all other offers
            for offer in offers:
                if offer.id != accepted_offer.id:
                    Prices.refuse_offer_by_id(offer.id)
        return accepted_offer
            
            