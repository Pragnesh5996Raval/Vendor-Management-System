from rest_framework import serializers
from .models import VendorMst, HistoryPerformanceMst

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorMst
        fields = ['id', 'name', 'contact_details', 'address', 'vendor_code']

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryPerformanceMst
        fields = ['id', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate', 'vendor']