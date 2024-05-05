from django.db import models

# Create your models here.
class VendorMst(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=255, unique=True)
    
class HistoryPerformanceMst(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    vendor = models.ForeignKey(VendorMst, on_delete=models.CASCADE)