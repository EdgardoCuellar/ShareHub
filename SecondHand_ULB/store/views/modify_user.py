from django.shortcuts import render, redirect
from store.models.customer import Customer
from django.views import View

class ModifyUser(View):
    def get(self, request):
        # Get the customer to be modified
        user = Customer.get_customer_by_id(request.session.get('customer'))
        print(user)
        return render(request, 'modify_user.html', {'user': user})

    def post(self, request):
        # Get the customer to be modified
        user = Customer.get_customer_by_id(request.session.get('customer'))

        # Handle the form submission and update customer information
        if request.method == 'POST':
            # Get form values
            if request.method == 'POST':
                # Get form values
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                password = request.POST.get('password')
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
                if description:
                    user.description = description

                # Save the updated user
                user.save()

        return redirect('profile')
