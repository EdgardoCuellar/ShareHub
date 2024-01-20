from django.db import models
from django.utils import timezone
from store.models.customer import Customer
from cryptography.fernet import Fernet

class Message(models.Model):
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='received_messages')
    encrypted_content = models.BinaryField(default=b"", blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} - {self.timestamp}"

    def encrypt_content(self, content, key):
        cipher_suite = Fernet(key)
        encrypted_content = cipher_suite.encrypt(content.encode('utf-8'))
        self.encrypted_content = encrypted_content
        return key

    def decrypt_content(self, key):
        cipher_suite = Fernet(key)
        decrypted_content = cipher_suite.decrypt(self.encrypted_content).decode('utf-8')
        return decrypted_content

    @staticmethod
    def get_messages_between(sender, receiver):
        messages = Message.objects.filter(sender=sender, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=sender)
        messages = messages.order_by('id')
        return messages

    @staticmethod
    def send_message(sender_id, receiver_id, content):
        sender = Customer.get_customer_by_id(sender_id)
        receiver = Customer.get_customer_by_id(receiver_id)
        message = Message(sender=sender)
        key = message.encrypt_content(content)
        message.receiver = receiver
        message.save()
        return key
