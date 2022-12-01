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
        Accommodation.objects.create(name="Python", code=123, owner=self.test_user)
        Accommodation.objects.create(name="Docker", code=789, owner=self.test_user)

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
        self.mock_locations = [
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

        for mock_name, mock_location in zip(self.mock_names, self.mock_locations):
            Accommodation.objects.create(name=mock_name, code=mock_location, owner=self.test_user)

    def test_accommodation_model(self):
        """Accommodation creation are correctly identified"""
        python_accommodation = Accommodation.objects.get(name="Python")
        docker_accommodation = Accommodation.objects.get(name="Docker")
        self.assertEqual(python_accommodation.owner.username, "testuser")
        self.assertEqual(docker_accommodation.owner.username, "testuser")
        self.assertEqual(python_accommodation.code, 123)
        self.assertEqual(docker_accommodation.code, 789)

    def test_accommodation_list(self):
        for mock_name, mock_location in zip(self.mock_names, self.mock_locations):
            accommodation_test = Accommodation.objects.get(name=mock_name)
            self.assertEqual(accommodation_test.owner.username, "testuser")
            self.assertEqual(accommodation_test.code, mock_location)