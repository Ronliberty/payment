from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'transaction_type', 'status', 'timestamp')
    list_filter = ('transaction_type', 'status', 'timestamp')
    search_fields = ('sender__email', 'receiver__email', 'transaction_type', 'status')
    ordering = ('-timestamp',)
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        """
        Export selected transactions as a CSV report.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Sender', 'Receiver', 'Amount', 'Type', 'Status', 'Date'])

        for transaction in queryset:
            writer.writerow([
                transaction.id,
                transaction.sender.email if transaction.sender else 'N/A',
                transaction.receiver.email if transaction.receiver else 'N/A',
                transaction.amount,
                transaction.transaction_type,
                transaction.status,
                transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])

        return response

    export_as_csv.short_description = "Print Report (Download CSV)"
