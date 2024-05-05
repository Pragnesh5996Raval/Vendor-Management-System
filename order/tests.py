from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Purchase_Order
from vendor.models import VendorMst

class PurchaseOrderAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = VendorMst.objects.create(name='Test Vendor', contact_details='test@example.com', address='123 Test St', vendor_code='12345')
        self.purchase_order_data = {
            'po_number': 'PO123',
            'items': {'item1': 'description1', 'item2': 'description2'},
            'quantity': 10,
            'status': 'pending',
            'quality_rating': 4.5,
            'vendor': self.vendor.id
        }
        self.purchase_order = Purchase_Order.objects.create(**self.purchase_order_data)

    def test_create_purchase_order(self):
        url = reverse('purchase-order-list-create')
        response = self.client.post(url, self.purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Purchase_Order.objects.count(), 2)

    def test_retrieve_purchase_order(self):
        url = reverse('purchase-order-retrieve-update-destroy', kwargs={'po_id': self.purchase_order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], self.purchase_order_data['po_number'])

    def test_update_purchase_order(self):
        updated_data = {
            'po_number': 'PO456',
            'status': 'completed',
            'quality_rating': 4.8,
        }
        url = reverse('purchase-order-retrieve-update-destroy', kwargs={'po_id': self.purchase_order.id})
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.po_number, updated_data['po_number'])

    def test_delete_purchase_order(self):
        url = reverse('purchase-order-retrieve-update-destroy', kwargs={'po_id': self.purchase_order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Purchase_Order.objects.filter(id=self.purchase_order.id).exists())

    def test_acknowledge_purchase_order(self):
        url = reverse('acknowledge-purchase-order', kwargs={'po_id': self.purchase_order.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertIsNotNone(self.purchase_order.acknowledgment_date)

        # Test if average response time is updated for the vendor
        self.vendor.refresh_from_db()
        self.assertNotEqual(self.vendor.average_response_time, 0)

