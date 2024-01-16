from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from django.views import View

from store.models.customer import Customer
from store.models.product import Products
from store.models.orders import Order
from store.models.message import Message
from store.models.prices import Prices

import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
        subject = "Confirmation d'offre ShareHub ULB"
        message = f"Bonjour, votre commande pour le produit {offer.product.name} a été acceptée. Vous pouvez maintenant verifier la suite du processus d'achat sur notre site."
        from_email = "sharehub.ulb@gmail.com"
        recipient_list = [offer.buyer.email]  # Assuming you have an email field in your Customer model

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        offer.status = 2
        offer.date_status = datetime.datetime.today()
        offer.save()
        return redirect('sales')

