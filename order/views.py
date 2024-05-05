from rest_framework import generics, status
from rest_framework.response import Response
from .models import Purchase_Order
from .serializers import PurchaseOrderSerializer
from django.db.models import Avg, F

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Purchase_Order.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase_Order.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
    
class AcknowledgePurchaseOrderAPIView(generics.UpdateAPIView):
    queryset = Purchase_Order.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Recalculate average response time
        completed_orders = Purchase_Order.objects.filter(vendor=instance.vendor, status='completed').exclude(acknowledgment_date=None)
        response_time_avg = completed_orders.aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response_time'].total_seconds() / 3600 or 0
        instance.vendor.average_response_time = response_time_avg
        instance.vendor.save()

        return Response(serializer.data)
