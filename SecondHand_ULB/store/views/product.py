from django.shortcuts import render , redirect

from store.models.product import Products
from store.models.prices import Prices
from store.models.customer import Customer
from store.models.category import Category
from store.models.rating import Rating
from django.views import  View

class Product(View):
    def get(self , request, product_id=None):
        if product_id is not None and Products.product_exists(product_id):
            product = Products.get_product_by_id(product_id)
            offer = Prices.get_price_by_buyer_product(request.session.get('customer') ,product_id)
            if offer:
                offer = offer[0]
            rating = Rating.get_rating(product.user_id)
            
            return render(request , 'product.html' , {'product' : product, 'product_offer': offer, 'rating': rating} )
        else:
            return redirect('store')

    def post(self , request, product_id=None):
        product = Products.get_product_by_id(product_id)
        rating = Rating.get_rating(product.user_id)
        if request.POST.get('offer'):
            offer = request.POST.get('offer')
        else:
            offer = Prices.get_price_by_buyer_product(request.session.get('customer') ,product_id)
            offer.delete()
            return render(request , 'product.html' , {'product' : product, 'product_offer': None, 'rating': rating} )

        offer = offer.replace(',', '.')        
        if not self.is_offer_valid(offer):
            return render(request , 'product.html' , {'product' : product, 'product_offer': None, 'rating': rating, 'error': 'Veuillez entrer un prix valide.'} )

        offer = int(float(offer) * 100)
        
        # create an offer
        new_offer = Prices(product=product,
                           seller=Customer.get_customer_by_id(product.user_id),
                           buyer=Customer.get_customer_by_id(request.session.get('customer')),
                           price=offer)
        new_offer.save()

        return render(request , 'product.html' , {'product' : product, 'product_offer': new_offer, 'rating': rating} )

    def is_offer_valid(self, offer):
        #Check if the offer price is valid, it should be higher than the product price and should be a number
        if not offer:
            return False
        try: 
            offer = float(offer)
        except:
            return False
        if offer <= 0:
            return False
        return True

def remove(request, product_id):
    if request.session.get('customer') != Products.get_product_by_id(product_id).user_id:
        return redirect('store')
    Products.remove_product_by_id(product_id)
    return redirect('store')