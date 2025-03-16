from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.customers.models import Customer


class CustomerServiceTest(TestCase):

    def setUp(self):
        self.app_user = AppUser.objects.create(
            username="active_owner",
            email="active_owner@example.com",
            phone="+34123456789",
            password="123456",
            is_active=True,
        )
        self.customer = Customer.objects.create(user_id=self.app_user.id)
