from django.db import models
from django.utils import timezone
from store.models.customer import Customer
from cryptography.fernet import Fernet
import os

class Message(models.Model):
    # Message model that stores encrypted content between a sender and receiver
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='received_messages')
    encrypted_content = models.BinaryField(default=b"", blank=True, null=True)  # Stores encrypted message
    receiver_seen = models.BooleanField(default=False)  # Track if the receiver has seen the message
    timestamp = models.DateTimeField(default=timezone.now)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = self.get_key()  # Fetch encryption key from file

    def get_key(self):
        # Retrieves encryption key from a file
        key_file_path = './private/message_key.txt'
        with open(key_file_path, 'rb') as f:
            key = f.read()
        return key

    def __str__(self):
        # Return basic info of the message
        return f"From {self.sender} to {self.receiver} - {self.timestamp}"

    def encrypt_content(self, content):
        # Encrypt the message content using the Fernet encryption scheme
        cipher_suite = Fernet(self.key)
        encrypted_content = cipher_suite.encrypt(content.encode('utf-8'))
        self.encrypted_content = encrypted_content

    def decrypt_content(self):
        # Decrypt the message content
        cipher_suite = Fernet(self.key)
        decrypted_content = cipher_suite.decrypt(self.encrypted_content).decode('utf-8')
        return decrypted_content

    @staticmethod
    def get_messages_between(sender, receiver):
        # Get all messages exchanged between the sender and receiver
        messages = Message.objects.filter(sender=sender, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=sender)
        return messages.order_by('id')

    @staticmethod
    def send_message(sender_id, receiver_id, content):
        # Send a message by creating a new Message object and encrypting the content
        sender = Customer.get_customer_by_id(sender_id)
        receiver = Customer.get_customer_by_id(receiver_id)
        message = Message(sender=sender)
        key = message.encrypt_content(content)
        message.receiver = receiver
        message.save()
        return key
    
    @staticmethod
    def get_nb_unseen_msg(user):
        # Count the number of unseen messages for a user
        return Message.objects.filter(receiver=user, receiver_seen=False).count()
    
    @staticmethod
    def get_nb_unseen_msg_per_sender(user, sender):
        # Get unseen messages for a user from a specific sender
        return Message.objects.filter(receiver=user, sender=sender, receiver_seen=False).count()
    
    @staticmethod
    def set_msg_seen(user, sender):
        # Mark messages from a sender as seen by updating the database
        Message.objects.filter(sender=sender, receiver=user, receiver_seen=False).update(receiver_seen=True)
