from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from store.models.customer import Customer
from store.models.message import Message

from django.utils.decorators import method_decorator
from store.utils.decorators import user_login_required

class MessagesView(View):

    html_template = "customer/message.html"

    key = b'0jneb-P_LUtlb_kEk3-Bx5hojBgnnidBLXOgBC_BgvE=' # Temporary secret key

    @method_decorator(user_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, receiver_id=None):

        sender = Customer.get_customer_by_id(request.session.get('customer'))
        receiver = None
        messages = None

        if receiver_id is not None:
            receiver = Customer.get_customer_by_id(receiver_id)
            messages = Message.get_messages_between(sender, receiver)
            if messages.count() > 0:
                for message in messages:
                    message.content = message.decrypt_content(self.key)
            else:
                decrypted_messages = None

        users_with_messages = self.get_users_with_messages(sender)

        context = {
            'sender': sender,
            'receiver': receiver,
            'messages': messages,
            'users_with_messages': users_with_messages,
        }

        return render(request, self.html_template, context)

    def get_users_with_messages(self, user):
        # Get a list of all users who have messages with the sender
        return Customer.objects.filter(
            Q(sent_messages__receiver=user) | Q(received_messages__sender=user)
        ).distinct()

    def post(self, request, receiver_id):
       
        sender_id = request.session.get('customer')
        sender = Customer.get_customer_by_id(sender_id)
        receiver = Customer.get_customer_by_id(receiver_id)

        content = request.POST.get('content')
        if content:
            message = Message(sender=sender)
            message.encrypt_content(content, self.key)
            message.receiver = receiver
            message.save()

        return redirect('messages', receiver_id=receiver_id)