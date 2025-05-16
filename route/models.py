from django.db import models

class Route(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True)  # Thêm dòng này
    departure_point = models.CharField(max_length=100, blank=True, null=True)
    destination_point = models.CharField(max_length=100, blank=True, null=True)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    estimated_time = models.TimeField(blank=True,null=True)
    description = models.CharField(max_length=255,blank=True,null=True)
    is_active = models.BooleanField(default=True,blank=False,null=False ) 
    
    class Meta:
        managed = False
        db_table = 'route'


