from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from mock import patch
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from consumers import models


class ReviewViewsTests(TestCase):
    """ Test whether our post entries show up on the posts page. """

    def setUp(self):
        self.company = models.Company.objects.create(name="Company X")
        self.user = User.objects.create_superuser(
            'superuser@example.com',
            email='superuser@example.com',
            password='superuser')

    @property
    def create_data(self):
        return {"rating": 5,
                "title": "Sample Review",
                "summary": "This is a test only review.",
                "ip_address": "123.123.123.123",
                "company": self.company.id}

    def test_create_behind_authentication(self):
        """ Test review creation endpoint requires authentication. """
        # Given
        url = reverse("review-list")

        # When
        response = self.client.post(url, self.create_data, format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(JSONWebTokenAuthentication, "authenticate_credentials")
    @patch("rest_framework_jwt.authentication.jwt_decode_handler")
    @patch.object(JSONWebTokenAuthentication, "get_jwt_value")
    def test_create(self, jwt_value_mock, jwt_decode_mock, jwt_cred_mock):
        """ Test review creation works as expected. """
        # Given
        url = reverse("review-list")

        # When
        jwt_value_mock.return_value = True
        jwt_decode_mock.return_value = True
        jwt_cred_mock.return_value = self.user
        response = self.client.post(url, self.create_data, format="json")

        # Then
        created_record = models.Review.objects.filter(
            title=self.create_data.get("title")).first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("id"), created_record.id)
