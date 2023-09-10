from django.shortcuts import render , redirect

from store.models.customer import Customer
from django.views import  View

class Profile(View):
    def get(self , request):
        user = request.session.get('customer')
        user = Customer.get_customer_by_id(user)

        return render(request , 'profile.html' , {'user' : user} )