from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View


class Signup (View):
    def get(self, request):
        return render (request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        error_message = None

        customer = Customer (first_name=first_name,
                             last_name=last_name,
                             email=email,
                             password=password)

        error_message = Customer.validateCustomer(customer)

        if not error_message:
            print (first_name, last_name, email, password)
            customer.password = make_password (customer.password)
            customer.register ()

            request.session['customer'] = customer.id
            return redirect ('login')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)
