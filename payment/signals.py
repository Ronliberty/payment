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


def save(self, *args, **kwargs):
    is_new = self.pk is None
    super().save(*args, **kwargs)

    if is_new:
        wallet = Wallet.objects.get(user=self.user)
        if self.transaction_type == 'deposit':
            wallet.balance += self.amount
        elif self.transaction_type == 'withdraw' or self.transaction_type == 'payment':
            wallet.balance -= self.amount
        elif self.transaction_type == 'send':
            wallet.balance -= self.amount
            if self.to_user:
                receiver_wallet, _ = Wallet.objects.get_or_create(user=self.to_user)
                receiver_wallet.balance += self.amount
                receiver_wallet.save()

                Transaction.objects.create(
                    user=self.to_user,
                    to_user=self.user,
                    transaction_type='receiver',
                    amount=self.amount,
                    description=f"Received from {self.user.email}"
                )

        wallet.save()
