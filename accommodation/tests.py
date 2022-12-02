import random
import string
from django.contrib.auth.models import User
from django.test import TestCase
from accommodation.models import Accommodation


class AccommodationTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="testuser",
            password="12345",
        )
        Accommodation.objects.create(name="Llao", contact=123, owner=self.test_user)
        Accommodation.objects.create(name="Francia", contact=789, owner=self.test_user)

        accommodation_test_num = 20
        self.mock_names = [
            "".join(
                [
                    random.choice((string.ascii_letters + string.digits))
                    for _ in range(random.randint(4, 20))
                ]
            )
            for _ in range(accommodation_test_num)
        ]
        self.mock_contacts = [
            int(
                "".join(
                    [
                        random.choice((string.digits))
                        for _ in range(random.randint(3, 9))
                    ]
                )
            )
            for _ in range(accommodation_test_num)
        ]

        for mock_name, mock_contact in zip(self.mock_names, self.mock_contacts):
            Accommodation.objects.create(name=mock_name, contact=mock_contact, owner=self.test_user)

    def test_accommodation_model(self):
        """Accommodation creation are correctly identified"""
        llao_accommodation = Accommodation.objects.get(name="Llao")
        francia_accommodation = Accommodation.objects.get(name="Francia")
        self.assertEqual(llao_accommodation.owner.username, "testuser")
        self.assertEqual(francia_accommodation.owner.username, "testuser")
        self.assertEqual(llao_accommodation.contact, 123)
        self.assertEqual(francia_accommodation.contact, 789)

    def test_course_list(self):
        for mock_name, mock_contact in zip(self.mock_names, self.mock_contacts):
            accommodation_test = Accommodation.objects.get(name=mock_name)
            self.assertEqual(accommodation_test.owner.username, "testuser")
            self.assertEqual(accommodation_test.contact, mock_contact)