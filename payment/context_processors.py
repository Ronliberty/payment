from decimal import Decimal
from payment.models import Wallet  # Make sure this import works

def wallet_balance_processor(request):
    if request.user.is_authenticated:
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        return {'wallet_balance': wallet.balance}
    return {'wallet_balance': Decimal('0.00')}