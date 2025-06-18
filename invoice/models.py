from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Chờ thanh toán'), ('paid', 'Đã thanh toán'), ('failed', 'Thất bại')],
        default='pending'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=[('cod', 'Thanh toán khi lên xe'), ('momo', 'Momo'), ('vnpay', 'VNPay')],
        default='cod'
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f'Invoice #{self.id} - {self.user.username}'
    class Meta:
        db_table = 'Invoice'

class PaymentTransaction(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='transactions')
    gateway = models.CharField(max_length=20, choices=[('momo', 'Momo'), ('vnpay', 'VNPay')])
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('success', 'Thành công'), ('failed', 'Thất bại')])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.gateway.upper()} - {self.transaction_id}'
    class Meta:
        db_table = 'PaymentTransaction'
