from django.db import models

# Create your models here.
class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=125,blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    driving_license = models.BigIntegerField( blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'driver'
