from django.db import models
from django.utils import timezone
from store.models.customer import Customer

class Message(models.Model):
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} - {self.timestamp}"

    
    @staticmethod
    def send_message(sender_id, receiver_id, content):
        sender = Customer.get_customer_by_id(sender_id)
        receiver = Customer.get_customer_by_id(receiver_id)
        message = Message(sender=sender, receiver=receiver, content=content)
        message.save()