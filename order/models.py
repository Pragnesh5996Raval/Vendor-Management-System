from django.db import models
from vendor.models import VendorMst

# Create your models here.
class Purchase_Order(models.Model):
    po_number = models.CharField(max_length=255)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('completed', 'completed'),
        ('canceled', 'canceled')
    )
    status = models.CharField(max_length=9, choices=STATUS_CHOICES)
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(blank=True, null=True)
    vendor = models.ForeignKey(VendorMst, on_delete=models.CASCADE)