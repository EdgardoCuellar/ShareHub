from django.contrib import admin
from django.urls import path

from .views.homepage import Homepage
from .views.home import Index , store
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart
from .views.offers import Offers
from .views.checkout import CheckOut
from .views.orders import OrderView
from .views.sales import Sales
from .views.sell import Sell
from .views.profile import Profile
from .views.product import Product, remove
from .views.message import MessagesView
from .views.modify_user import ModifyUser
from .views.modify_product import ModifyProduct
from .views.my_products import MyProductsView
from .views.forgot_password import ForgoPasswordView

from .middlewares.auth import  auth_middleware

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('store', store , name='store'),

    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('offers', auth_middleware(Offers.as_view()) , name='offers'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('sell', Sell.as_view(), name='sell'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('sales', auth_middleware(Sales.as_view()), name='sales'),
    path('profile', Profile.as_view(), name='profile'),
    path('profile/<int:user_id>', Profile.as_view(), name='profile'),
    path('product', store, name='store'),
    path('product/<int:product_id>', Product.as_view(), name='product'),
    path('product/remove/<int:product_id>', remove, name='product_remove'),
    path('modify_user', ModifyUser.as_view(), name='modify_user'),
    path('my_products', auth_middleware(MyProductsView.as_view()), name='my_products'),
    path('modify_product', store, name='store'),
    path('modify_product/<int:product_id>', ModifyProduct.as_view(), name='modify_product'),
    path('message', MessagesView.as_view(), name='messages'),
    path('message/<int:receiver_id>', MessagesView.as_view(), name='messages'),
    path('forgot_password/', ForgoPasswordView.as_view(), name='forgot_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)