from django.shortcuts import render , redirect
from django.contrib.auth.hashers import make_password

from store.models.customer import Customer
from store.models.rating import Rating
from store.models.category import Category
from store.models.product import Products
from store.models.orders import Order
from django.views import  View

from django.utils.decorators import method_decorator
from store.utils.decorators import user_login_required

class DashboardView(View):

    html_template = "customer/dashboard.html"

    @method_decorator(user_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self , request, page=None):
        if not page or page not in ['account', 'modify_user', 'my_products', 'orders']:
            page = 'profile'

        user_id = request.session.get('customer')
        user = Customer.get_customer_by_id(user_id)

        user.faculty = Category.get_category_by_id(user.faculty).name

        rating = Rating.get_rating(user.id)

        categories = None
        products = None
        orders = None
        if page == 'modify_user':
            categories = Category.get_all_categories_except_last()
        elif page == 'my_products':
            products = Products.get_products_by_userid(user.id)
        elif page == 'orders':
            orders = Order.get_orders_by_buyer(user.id)

        error = request.session.get('error')
        if error:
            del request.session['error']

        return render(request , self.html_template , {
            'page': page,
            'user' : user,
            "rating": rating,
            "categories": categories,
            "products": products,
            "orders": orders,
            "error": error
        } )

    def post(self, request, page=None):
        if not page:
            redirect('dashboard')

        if page == 'modify_user':
            return self.modify_user(request)

        if page == 'orders':
            return self.orders(request)


    def modify_user(self, request):
        # Get the customer to be modified
        user = Customer.get_customer_by_id(request.session.get('customer'))
        error_message = None
        # Handle the form submission and update customer information
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

    def orders(self, request):
        order_id = request.POST.get('order_id')
        rating_score = int(request.POST.get('rating'))

        # Get the order object
        order = Order.get_order_by_id(order_id)

        # Update the order's user_rating with the submitted rating_score
        rating = Rating(user_id=order.seller.id, user_rated_id=order.buyer.id, rating=rating_score)
        order.rated = rating_score
        rating.save()
        order.save()

        return redirect('dashboard', page='orders')
