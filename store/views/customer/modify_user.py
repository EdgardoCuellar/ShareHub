from django.shortcuts import render, redirect

from store.models.category import Category
from store.models.customer import Customer

from django.contrib.auth.hashers import make_password
from django.views import View

class ModifyUser(View):

    html_template = "customer/modify_user.html"

    def get(self, request):
        # Get the customer to be modified
        if not request.session.get('customer'):
            return redirect('login')
        user = Customer.get_customer_by_id(request.session.get('customer'))
        categories = Category.get_all_categories()
        return render(request, self.html_template, {'user': user, 'categories': categories})

    def post(self, request):
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
            faculty = request.POST.get('faculty')
            description = request.POST.get('description')

            # Update fields only if they are not empty
            if first_name:
                user.first_name = first_name
            if first_name:
                user.last_name = last_name
            if email:
                user.email = email
            if password:
                user.password = password
            if faculty:
                user.faculty = Category.get_category_by_name(faculty).id
            if description:
                user.description = description
            
            error_message = Customer.validateCustomer(user, True)
            if not error_message:
                user.password = make_password(user.password)
                user.save()
                return redirect('profile')

        categories = Category.get_all_categories()
        return render(request, self.html_template, {'user': user, 'categories': categories, 'error': error_message})
