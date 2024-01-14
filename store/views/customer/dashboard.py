from django.shortcuts import render , redirect
from django.contrib.auth.hashers import make_password

from store.models.customer import Customer
from store.models.rating import Rating
from store.models.category import Category
from django.views import  View

class DashboardView(View):

    html_template = "customer/dashboard.html"

    def get(self , request, page=None):
        if not request.session.get('customer'):
            return redirect('login')
        if not page:
            page = 'profile'

        user_id = request.session.get('customer')
        user = Customer.get_customer_by_id(user_id)

        user.faculty = Category.get_category_by_id(user.faculty).name

        rating = Rating.get_rating(user.id)

        categories = Category.get_all_categories()

        error = request.session.get('error')
        if error:
            del request.session['error']

        return render(request , self.html_template , {
            'page': page,
             'user' : user,
              "rating": rating,
               "categories": categories,
                "error": error
        } )

    def post(self, request, page=None):
        if not request.session.get('customer'):
            return redirect('login')
        if not page:
            redirect('dashboard')

        # Get the customer to be modified
        user = Customer.get_customer_by_id(request.session.get('customer'))
        error_message = None
        # Handle the form submission and update customer information
        if request.method == 'POST':
            # Get form values
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            faculty = request.POST.get('faculty')
            description = request.POST.get('description')

            # Update fields only if they are not empty
            if first_name:
                user.first_name = first_name
            if first_name:
                user.last_name = last_name
            if email:
                user.email = email
            if password and confirm_password and password == confirm_password:
                user.password = password
            if faculty:
                user.faculty = Category.get_category_by_name(faculty).id
            if description:
                user.description = description
            
            error_message = Customer.validateCustomer(user, True)
            if not error_message:
                user.password = make_password(user.password)
                user.save()
                return redirect('dashboard', page="account")

        categories = Category.get_all_categories()

        request.session['error'] = error_message

        return redirect('dashboard', page="modify_user")
