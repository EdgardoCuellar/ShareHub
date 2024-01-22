from django.shortcuts import render, redirect
from store.models.product import Products
from store.models.category import Category, Condition, Place
from django.views import View
from datetime import datetime
from store.models.customer import Customer
from store.models.product_img import ProductImage

from django.utils.decorators import method_decorator
from store.utils.decorators import user_login_required

from django.http import JsonResponse
from django.urls import reverse

class ModifyProduct (View):

    html_template = "products/modify_product.html"

    @method_decorator(user_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, product_id):
        if request.session.get('customer') != Products.get_product_by_id(product_id).customer.id or Products.get_product_by_id(product_id).sold:
            return redirect('homepage')

        categories = Category.get_all_categories()
        conditions = Condition.get_all_conditions()
        places = Place.get_all_places()
        product = Products.get_product_by_id(product_id)
        product.price = product.price / 100

        error = request.session.get('error')
        if error:
            del request.session['error']

        return render (request, self.html_template, {
            'product': product,
            'error': error,
            'categories': categories, 
            'conditions': conditions, 
            'places': places})

    def post(self, request, product_id):
        if request.session.get('customer') != Products.get_product_by_id(product_id).customer.id:
            return redirect('homepage')
        
        product = Products.get_product_by_id(product_id)
        if request.method == 'POST':
            name = request.POST.get('name')
            price = request.POST.get('price')
            date = request.POST.get('date')
            faculty = request.POST.get('faculty')
            condition = request.POST.get('condition')
            place = request.POST.get('place')
            description = request.POST.get('description')
            length = int(request.POST.get('length'))

            if name:
                product.name = name
            if price:
                price = Products.price_good_format(request.POST.get('price'))
                product.price = price
            if date:
                product.date = date
            if faculty:
                product.category = Category.get_category_by_name(faculty)
            if condition:
                product.condition = Condition.get_condition_by_name(condition)
            if place:
                product.place = Place.get_place_by_name(place)
            if description:
                product.description = description
            if length > 0:
                ProductImage.remove_images_by_product_id(product_id)

                for file_num in range(0, int(length)):
                    ProductImage.objects.create(
                    product=product,
                    image=request.FILES.get(f'images{file_num}')
                )

            error_message = product.validate_product()
            
            if not error_message:
                product.save()
                json = JsonResponse({'redirect_url': reverse('product', args=[product.id])})
                return json  # Redirect to the homepage or any other appropriate page after successful upload

        categories = Category.get_all_categories()
        condition = Condition.get_all_conditions()
        places = Place.get_all_places()

        request.session['error'] = error_message
        json = JsonResponse({'redirect_url': reverse('modify_product', args=[product.id])})
        return json
