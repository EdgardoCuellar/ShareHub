from django.contrib import admin
from django.urls import path

from .views.homepage import Homepage
from .views.home import Index , store
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.orders import OrderView
from .views.sell import Sell
from .views.profile import Profile
from .views.product import Product
from .views.message import MessagesView
from .views.modify_user import ModifyUser
from .views.modify_product import ModifyProduct

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
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('sell', Sell.as_view(), name='sell'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('profile', Profile.as_view(), name='profile'),
    path('profile/<int:user_id>', Profile.as_view(), name='profile'),
    path('product', store, name='store'),
    path('product/<int:product_id>', Product.as_view(), name='product'),
    path('modify_user', ModifyUser.as_view(), name='modify_user'),
    path('modify_product', store, name='store'),
    path('modify_product/<int:product_id>', ModifyProduct.as_view(), name='modify_product'),
    path('message', MessagesView.as_view(), name='messages'),
    path('message/<int:receiver_id>', MessagesView.as_view(), name='messages'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)