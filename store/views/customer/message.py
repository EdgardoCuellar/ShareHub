from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from store.models.customer import Customer
from store.models.message import Message

from django.utils.decorators import method_decorator
from store.utils.decorators import user_login_required

class MessagesView(View):

    html_template = "customer/message.html"

    @method_decorator(user_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, receiver_id=None):

        sender = Customer.get_customer_by_id(request.session.get('customer'))
        receiver = None
        messages = None

        if receiver_id is not None:
            receiver = Customer.get_customer_by_id(receiver_id)
            messages = Message.objects.filter(sender=sender, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=sender)
            # order the messages by message_id
            messages = messages.order_by('id')


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
            message = Message(sender=sender, receiver=receiver, content=content)
            message.save()

        messages = Message.objects.filter(sender=sender, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=sender)
        users_with_messages = self.get_users_with_messages(sender)

        context = {
            'sender': sender,
            'receiver': receiver,
            'messages': messages,
            'users_with_messages': users_with_messages,
        }

        return render(request, self.html_template, context)
