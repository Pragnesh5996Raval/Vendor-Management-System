from django.urls import path
from . import views

urlpatterns = [
    path('api/vendors/', views.VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:vendor_id>/', views.VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-retrieve-update-destroy'),
    path('api/vendors/<int:vendor_id>/performance/', views.VendorPerformanceAPIView.as_view(), name='vendor-performance'),
]
