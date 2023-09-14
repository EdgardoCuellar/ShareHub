from django.shortcuts import render, redirect
from store.models.product import Products
from store.models.category import Category, Condition
from django.views import View
from datetime import datetime


class Sell (View):
    def get(self, request):
        categories = Category.get_all_categories()
        conditions = Condition.get_all_conditions()
        return render (request, 'sell.html', {'categories': categories, 'conditions': conditions})

    def post(self, request):
        price = Products.transformPrice(request.POST.get('price'))
        product = Products(name=request.POST.get('name'),
                                price=price,
                                date=request.POST.get('date'),
                                category=Category.get_category_by_name(request.POST.get('category')),
                                condition=Condition.get_condition_by_name(request.POST.get('condition')),
                                description=request.POST.get('description'),
                                image=request.FILES.get('image'),
                                user_id=request.session.get('customer'))

        error_message = self.validateProduct(product)
        print(error_message)
        if not error_message:
            product.register()
            return redirect('store')  # Redirect to the homepage or any other appropriate page after successful upload

        categories = Category.get_all_categories()
        conditions = Condition.get_all_conditions()
        return render(request, 'sell.html', {'categories': categories, 'conditions': conditions, 'error': error_message})

    def validateProduct(self, product_validation):
        error_message = None
        if (not product_validation.name):
            error_message = "Vous devez entrer un nom !"
        elif len (product_validation.name) < 3:
            error_message = 'Le nom doit contenir au moins 3 caractères'
        elif len (product_validation.name) > 80:
            error_message = 'Le nom ne peut pas contenir plus de 80 caractères'
        elif int(product_validation.price) < 100 or int(product_validation.price) > 10000:
            error_message = "Le prix doit se trouver entre 1 et 100 €" 
        elif int(product_validation.date) < 2000:
            error_message = "L'année d'achat doit etre au minimum 2000" 
        elif int(product_validation.date) > datetime.now().year:
            error_message = "L'année d'achat ne peut pas être dans le futur"
        elif product_validation.description and len(product_validation.description) >= 300:
            error_message = "La description ne peut pas dépasser 300 caractères"
        elif len(product_validation.description) <= 10:
            error_message = "La description doit au moins faire 10 caractères"

        # Add file upload validation
        if not self.validate_image(product_validation.image):
            error_message = "L'image doit être au format .jpg ou .png, avoir une taille inférieure à 5 Mo et des dimensions minimales de 250x300 pixels."

        return error_message

    def validate_image(self, image):
            # Check if the uploaded file is an image
        if not image:
            return False
        ext = image.name.split('.')[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png']:
            return False

        # Check file size (less than 5MB)
        if image.size > 5 * 1024 * 1024:  # 5MB
            return False

        # Check image dimensions (at least 250x300 pixels)
        from PIL import Image
        img = Image.open(image)
        width, height = img.size
        if width < 250 or height < 300:
            return False

        return True