from django.contrib import admin
from .models.product import Products
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from .models.prices import Prices
from .models.rating import Rating
from .models.product_img import ProductImage
from .models.message import Message
from .models.forgot_password import ForgotPassword


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Products,AdminProduct)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Prices)
admin.site.register(Rating)
admin.site.register(ProductImage)
admin.site.register(Message)
admin.site.register(ForgotPassword)


# username = Tanushree, email = tanushree7252@gmail.com, password = 1234
