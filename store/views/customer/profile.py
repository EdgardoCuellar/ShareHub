from django.shortcuts import render , redirect

from store.models.customer import Customer
from store.models.rating import Rating
from store.models.category import Category
from django.views import  View

class Profile(View):

    html_template = "customer/profile.html"

    def get(self , request, user_id=None):
        same_user = True
        if user_id is not None and Customer.user_exists(user_id):
            user = Customer.get_customer_by_id(user_id)
            my_user = request.session.get('customer')
            my_user = Customer.get_customer_by_id(my_user)
            if user.id != my_user.id:
                same_user = False
        else:
            user = request.session.get('customer')
            user = Customer.get_customer_by_id(user)

        user.faculty = Category.get_category_by_id(user.faculty).name

        rating = Rating.get_rating(user.id)

        return render(request , self.html_template , {'user' : user, "rating": rating} )