from django.db import models
from datetime import timedelta

class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey('driver.Driver', on_delete=models.SET_NULL, null=True, related_name='trips')
    vehicle = models.ForeignKey('vehicle.Vehicle', on_delete=models.SET_NULL, null=True, related_name='trips')
    route = models.ForeignKey('route.Route', on_delete=models.SET_NULL, null=True, related_name='trips')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(blank=True, null=True, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if self.route and self.route.estimated_time and self.departure_time:
            est_time = self.route.estimated_time
            self.arrival_time = self.departure_time + timedelta(
                hours=est_time.hour,
                minutes=est_time.minute,
                seconds=est_time.second
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Chuyến #{self.id} - {self.route.code} ({self.departure_time.strftime('%d/%m/%Y %H:%M')})"
    class Meta:
        db_table = 'trip'
        managed = False
        verbose_name = "Chuyến đi"
        verbose_name_plural = "Các chuyến đi"
        ordering = ['-departure_time']
