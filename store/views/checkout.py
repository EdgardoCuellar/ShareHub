from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from django.views import View

from store.models.customer import Customer
from store.models.product import Products
from store.models.orders import Order
from store.models.message import Message
from store.models.prices import Prices

import time

from store.utils.send_email import send_mail_sell, send_mail_buy

class CheckOut(View):
    def post(self, request):
        offer_id = int(request.POST.get('offer'))
        offer = Prices.get_price_by_id(offer_id)

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
        message = Message(sender=offer.seller,
                            receiver=offer.buyer,
                            product=offer.product,
                            content="Votre offre a été acceptée. Vous pouvez contacter le vendeur pour plus d'informations.")

        offer.status = 2
        offer.timestamp_status = time.time()
        offer.save()
        return redirect('sales')

