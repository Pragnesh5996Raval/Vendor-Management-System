from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from order.models import Purchase_Order 
from .models import VendorMst, HistoryPerformanceMst
from .serializers import VendorSerializer, VendorPerformanceSerializer
from django.db.models import Avg, F

# Create your views here.
class VendorListCreateAPIView(APIView):
    def get(self, request):
        vendors = VendorMst.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, vendor_id):
        try:
            return VendorMst.objects.get(pk=vendor_id)
        except VendorMst.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    
    def put(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        vendor.delete()
        return Response({"Message":"Vendor deleted successfully."}, status=status.HTTP_200_OK)
    
class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = VendorMst.objects.get(pk=vendor_id)
            completed_orders = Purchase_Order.objects.filter(vendor=vendor, status='completed')

            # On-Time Delivery Rate
            total_completed_orders = completed_orders.count()
            on_time_delivery_count = completed_orders.filter(delivery_date__lte=F('delivery_date')).count()
            on_time_delivery_rate = (on_time_delivery_count / total_completed_orders) * 100 if total_completed_orders > 0 else 0

            # Quality Rating Average
            quality_rating_avg = completed_orders.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating'] or 0

            # Average Response Time
            response_time_avg = completed_orders.exclude(acknowledgment_date=None).aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response_time'].total_seconds() / 3600 or 0

            # Fulfilment Rate
            fulfilled_count = completed_orders.filter(status='completed', quality_rating__isnull=False).count()
            fulfillment_rate = (fulfilled_count / total_completed_orders) * 100 if total_completed_orders > 0 else 0

            # Return performance metrics
            performance_metrics = HistoryPerformanceMst.objects.create(
                vendor=vendor,
                on_time_delivery_rate=on_time_delivery_rate,
                quality_rating_avg=quality_rating_avg,
                average_response_time=response_time_avg,
                fulfillment_rate=fulfillment_rate
            )
            vendor_performance = VendorPerformanceSerializer(performance_metrics)
            return Response(vendor_performance.data, status=status.HTTP_201_CREATED)
        except VendorMst.DoesNotExist:
            print("yes")
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)