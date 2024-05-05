from django.urls import path
from . import views

urlpatterns = [
    path('api/purchase_orders/', views.PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<int:po_id>/', views.PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase-order-retrieve-update-destroy'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', views.AcknowledgePurchaseOrderAPIView.as_view(), name='acknowledge-purchase-order'),
]
