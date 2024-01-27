from django.shortcuts import render , redirect

from store.models.product import Products
from store.models.prices import Prices
from store.models.customer import Customer
from store.models.category import Category
from store.models.rating import Rating
from store.models.product_img import ProductImage
from django.views import  View

class Product(View):

    html_template = "products/product.html"

    def get(self , request, product_id=None):
        if product_id is not None and Products.product_exists(product_id):
            product = Products.get_product_by_id(product_id)
            offer = Prices.get_price_by_buyer_product(request.session.get('customer') ,product_id)
            if offer:
                offer = offer[0]
            rating = Rating.get_rating(product.customer.id)
            nb_offers = len(Prices.get_prices_by_product_id(product_id))
            return render(request , self.html_template , {'product' : product, 'product_offer': offer, 'rating': rating, 'nb_offers': nb_offers} )
        else:
            return redirect('index')

    def post(self , request, product_id=None):
        product = Products.get_product_by_id(product_id)
        rating = Rating.get_rating(product.customer.id)
        nb_offers = len(Prices.get_prices_by_product_id(product_id))
        if request.POST.get('offer'):
            offer = request.POST.get('offer')
        else:
            offer = Prices.get_price_by_buyer_product(request.session.get('customer') ,product_id)
            offer.delete()
            return render(request , self.html_template , {'product' : product, 'product_offer': None, 'rating': rating, 'nb_offers': nb_offers} )

        offer = offer.replace(',', '.')        
        
        offer = int(float(offer) * 100)
        
        # create an offer
        new_offer = Prices(product=product,
                           seller=Customer.get_customer_by_id(product.customer.id),
                           buyer=Customer.get_customer_by_id(request.session.get('customer')),
                           price=offer,
                           status=0)
        new_offer.save()

        return render(request , self.html_template , {'product' : product, 'product_offer': new_offer, 'rating': rating, 'nb_offers': nb_offers} )


def remove(request, product_id):
    if request.session.get('customer') != Products.get_product_by_id(product_id).customer.id:
        return redirect('index')

    ProductImage.remove_images_by_product_id(product_id)

    Products.remove_product_by_id(product_id)
    return redirect('index')