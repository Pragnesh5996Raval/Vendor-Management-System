from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import VendorMst

class VendorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Test St',
            'vendor_code': '12345'
        }
        self.vendor = VendorMst.objects.create(**self.vendor_data)

    def test_create_vendor(self):
        response = self.client.post('/api/vendors/', self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VendorMst.objects.count(), 2)  # One vendor was created in setUp

    def test_retrieve_vendor(self):
        response = self.client.get(f'/api/vendors/{self.vendor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor_data['name'])

    def test_update_vendor(self):
        updated_data = {
            'name': 'Updated Vendor',
            'contact_details': 'updated_test@example.com',
            'address': '456 Updated St',
            'vendor_code': '54321'
        }
        response = self.client.put(f'/api/vendors/{self.vendor.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, updated_data['name'])

    def test_delete_vendor(self):
        response = self.client.delete(f'/api/vendors/{self.vendor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(VendorMst.objects.filter(id=self.vendor.id).exists())

    def test_vendor_performance(self):
        response = self.client.get(f'/api/vendors/{self.vendor.id}/performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions for performance metrics if needed

    # Additional tests can be added for edge cases, error handling, etc.

