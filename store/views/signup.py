from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from store.models.customer import Customer
from store.models.category import Category
from django.views import View

class Signup(View):
    def get(self, request):
        categories = Category.get_all_categories()
        return render(request, 'signup.html', {'categories': categories})

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        faculty = postData.get('faculty')
        email = postData.get('email')
        password = postData.get('password')

        # Validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            faculty=faculty,
                            email=email,
                            password=password)

        error_message = Customer.validateCustomer(customer)

        if not error_message:
            # Hash the password before saving
            hashed_password = make_password(customer.password)
            customer.password = hashed_password

            customer.register()

            request.session['customer'] = customer.id
            return redirect('product')
        else:
            data = {
                'error': error_message,
                'values': value,
                'categories': Category.get_all_categories()
            }
            return render(request, 'signup.html', data)
