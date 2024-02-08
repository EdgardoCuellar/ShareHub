from django.db import models
from django.utils import timezone
from store.models.customer import Customer
from cryptography.fernet import Fernet
import os

class Message(models.Model):
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='received_messages')
    encrypted_content = models.BinaryField(default=b"", blank=True, null=True)
    receiver_seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = self.get_key()

    def get_key(self):
        key_file_path = './private/message_key.txt'
        key = ""

        # if not os.path.isfile(key_file_path):
        #     # Generate a new key if the file doesn't exist
        #     key = Fernet.generate_key()
        #     with open(key_file_path, 'wb') as key_file:
        #         key_file.write(key)
        # else:
        with open(key_file_path, 'rb') as f:
            key = f.read()

        return key


    def __str__(self):
        return f"From {self.sender} to {self.receiver} - {self.timestamp}"

    def encrypt_content(self, content):
        cipher_suite = Fernet(self.key)
        encrypted_content = cipher_suite.encrypt(content.encode('utf-8'))
        self.encrypted_content = encrypted_content

    def decrypt_content(self):
        cipher_suite = Fernet(self.key)
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
    
    @staticmethod
    def get_nb_unseen_msg(user):
        nb_unseen = Message.objects.filter(receiver=user, receiver_seen=False).count()
        return nb_unseen
    
    @staticmethod
    def get_nb_unseen_msg_per_sender(user, sender):
        nb_unseen = Message.objects.filter(receiver=user, sender=sender, receiver_seen=False).count()
        return nb_unseen
    
    @staticmethod
    def set_msg_seen(user, sender):
        Message.objects.filter(sender=sender, receiver=user, receiver_seen=False).update(receiver_seen=True)
