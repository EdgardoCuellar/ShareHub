from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.models.orders import Order
from store.models.rating import Rating
from store.middlewares.auth import auth_middleware

class OrderView(View):


    def get(self , request ):
        if not request.session.get('customer'):
            return redirect('login')

        customer = request.session.get('customer')
        orders = Order.get_orders_by_buyer(customer)
        
        return render(request , 'orders.html'  , {'orders' : orders})

    def post(self, request):
            # Retrieve data from the POST request
        order_id = request.POST.get('order_id')
        rating_score = int(request.POST.get('rating'))

        # Get the order object
        order = Order.get_order_by_id(order_id)

        # Update the order's user_rating with the submitted rating_score
        rating = Rating(user_id=order.seller.id, user_rated_id=order.buyer.id, rating=rating_score)
        rating.save()

        return redirect('orders')




