from django.db import models
class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    trip = models.ForeignKey('trip.Trip', on_delete=models.CASCADE)  # chuyendi
    seat_number = models.CharField(max_length=10)               # soghe
    status = models.CharField(max_length=50)                    # trangthai
    passenger_name = models.CharField(max_length=100, blank=True, null=True)
    passenger_phone = models.CharField(max_length=15, blank=True, null=True)
    passenger_email = models.EmailField(blank=True, null=True)                    # emailnguoidi
    invoice = models.ForeignKey('invoice.Invoice', on_delete=models.SET_NULL, null=True, blank=True)  # hoadon
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True) # khachhang
    luggage_weight = models.IntegerField(blank=True,null=True)
    has_child_under_6 = models.BooleanField(default=False)
    pickup_point = models.CharField(max_length=255, blank=True, null=True)
    reserved_until = models.DateTimeField(null=True, blank=True)  # giữ đến thời điểm này

    class Meta:
        managed = False
        unique_together = ('trip', 'seat_number')
        db_table = 'ticket'
            