# Generated by Django 4.2.19 on 2025-03-30 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_transaction_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
