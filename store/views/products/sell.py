from django.shortcuts import render, redirect
from store.models.product import Products
from store.models.product_img import ProductImage
from store.models.customer import Customer
from store.models.category import Category, Condition, Place
from django.views import View
from datetime import datetime

from django.utils.decorators import method_decorator
from store.utils.decorators import user_login_required

class Sell (View):

    html_link = 'products/sell.html'

    @method_decorator(user_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        categories = Category.get_all_categories()
        conditions = Condition.get_all_conditions()
        places = Place.get_all_places()
        
        error_message = request.session.get('error_message')
        if error_message:
            del request.session['error_message']
        if request.session.get('success'):
            product_id = request.session.get('success')
            del request.session['success']
            return redirect('product', product_id)

        return render (request, self.html_link, {'categories': categories, 'conditions': conditions, 'places': places, 'error_message': error_message})

    def post(self, request):
        price = Products.price_good_format(request.POST.get('price'))
        print(price)
        customer_id = request.session.get('customer')
        customer = Customer.get_customer_by_id(customer_id)
        product = Products(name=request.POST.get('name'),
                                price=price,
                                date=request.POST.get('date'),
                                category=Category.get_category_by_name(request.POST.get('category')),
                                condition=Condition.get_condition_by_name(request.POST.get('condition')),
                                place=Place.get_place_by_name(request.POST.get('place')),
                                description=request.POST.get('description'),
                                customer=customer)

        error_message = product.validate_product()
        
        if not error_message:
            product.register()

            length = request.POST.get('length')
            for file_num in range(0, int(length)):
                ProductImage.objects.create(
                    product=product,
                    image=request.FILES.get(f'images{file_num}')
                )
            request.session['success'] = product.id
            return redirect('index')  # Redirect to the homepage or any other appropriate page after successful upload

        request.session['error_message'] = error_message

        return redirect('index')