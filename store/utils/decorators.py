from functools import wraps
from django.shortcuts import redirect
from store.models.customer import Customer

def user_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('customer'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper