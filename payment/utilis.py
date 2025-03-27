from cryptography.fernet import Fernet
from django.conf import settings

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(data):
    return cipher_suite.decrypt(data.encode()).decode()
