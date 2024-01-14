from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.models.orders import Order
from store.middlewares.auth import auth_middleware

from django.utils.decorators import method_decorator
from store.utils.decorators import user_login_required

class Sales(View):

    @method_decorator(user_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self , request ):
        if not request.session.get('customer'):
            return redirect('login')

        seller = request.session.get('customer')
        orders = Order.get_orders_by_seller(seller)
        
        return render(request , 'sales.html'  , {'orders' : orders})


    def post(self, request):
        order = request.POST.get('order')
        order = Order.objects.get(id=order)

        status = request.POST.get('status')
        place_description = request.POST.get('place_description')

        if status:
            order.status = True
        if place_description:
            order.place_description = place_description
        order.save()

        return redirect('sales')

