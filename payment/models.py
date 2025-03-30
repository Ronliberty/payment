from django.conf import settings
from django.db import models
import random
import uuid
from django.db import transaction as db_transaction

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default="USD")

    def __str__(self):
        return f"{self.user.username} - {self.balance} {self.currency}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('payment_request', 'Payment Request')
    ]

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_transactions', null=True, blank=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_transactions', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    processed = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"

    def process_transaction(self):
        """
        Atomically updates wallets based on transaction type.
        Handles concurrency using select_for_update and database transactions.
        """
        if self.status != 'completed' or self.processed:
            return

        try:
            with db_transaction.atomic():
                # Lock transaction and wallets for atomic update
                transaction = Transaction.objects.select_for_update().get(pk=self.pk)

                if transaction.transaction_type == 'deposit':
                    self._process_deposit()
                elif transaction.transaction_type == 'withdrawal':
                    self._process_withdrawal()
                elif transaction.transaction_type in ['transfer', 'payment_request']:
                    self._process_transfer()




                transaction.processed = True
                transaction.save(update_fields=['processed'])

        except Exception as e:
            self.status = 'failed'
            self.save(update_fields=['status'])
            raise e

    def _process_deposit(self):
        """Handle deposit to receiver's wallet"""
        if not self.receiver:
            raise ValueError("Deposit requires a receiver")

        wallet = Wallet.objects.select_for_update().get(user=self.receiver)
        wallet.balance += self.amount
        wallet.save()

    def _process_withdrawal(self):
        """Handle withdrawal from sender's wallet"""
        if not self.sender:
            raise ValueError("Withdrawal requires a sender")

        wallet = Wallet.objects.select_for_update().get(user=self.sender)
        if wallet.balance < self.amount:
            raise ValueError("Insufficient funds for withdrawal")
        wallet.balance -= self.amount
        wallet.save()

    def _process_transfer(self):
        """Handle transfer between sender and receiver"""
        if not self.sender or not self.receiver:
            raise ValueError("Transfer requires both sender and receiver")

        sender_wallet = Wallet.objects.select_for_update().get(user=self.sender)
        receiver_wallet = Wallet.objects.select_for_update().get(user=self.receiver)

        if sender_wallet.balance < self.amount:
            raise ValueError("Insufficient funds for transfer")

        sender_wallet.balance -= self.amount
        receiver_wallet.balance += self.amount
        sender_wallet.save()
        receiver_wallet.save()



class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def generate_code(self):
        self.code = str(random.randint(100000, 999999))
        self.save()
