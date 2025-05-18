from django.db import models

class Vehicle(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=125,blank=True,null=True)
    type = models.CharField(max_length=100,blank=True,null=True)
    chair = models.IntegerField(blank=True, null=True)
    licenseplate = models.CharField(max_length=125,blank=True,null=True)
    class Meta:
        managed = False
        db_table = 'vehicle'