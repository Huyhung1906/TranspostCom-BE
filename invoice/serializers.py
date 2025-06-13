# serializers.py
from rest_framework import serializers
from .models import Invoice, PaymentTransaction
from ticket.models import Ticket
from ticket.serializers import TicketSerializer  
class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    transactions = PaymentTransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'user', 'created_at', 'total_amount', 'status',
            'payment_method', 'transaction_id', 'tickets', 'transactions'
        ]
        read_only_fields = ['user', 'created_at', 'transaction_id']