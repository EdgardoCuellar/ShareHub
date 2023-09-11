from django.shortcuts import render , redirect

from store.models.customer import Customer
from django.views import  View

class Profile(View):
    def get(self , request, user_id=None):
        if user_id is not None and Customer.user_exists(user_id):
            user = Customer.get_customer_by_id(user_id)
            my_user = request.session.get('customer')
            my_user = Customer.get_customer_by_id(my_user)
            if user.id == my_user.id:
                print("same user")
        else:
            user = request.session.get('customer')
            user = Customer.get_customer_by_id(user)

        return render(request , 'profile.html' , {'user' : user} )