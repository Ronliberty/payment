from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OTP, Transaction, Wallet
from django.conf import settings

@receiver(post_save, sender=Transaction)
def generate_otp_for_transaction(sender, instance, **kwargs):
    if instance.transaction_type in ['transfer', 'withdrawal']:
        otp = OTP.objects.create(user=instance.sender)
        otp.generate_code()
        print(f"OTP for transaction: {otp.code}")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)