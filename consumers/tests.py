from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from mixer.backend.django import mixer
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
                "company": self.company.id}

    @property
    def object_create_data(self):
        return {"rating": 5,
                "title": "Sample Review",
                "summary": "This is a test only review.",
                "ip_address": "123.123.123.123",
                "company": self.company,
                "reviewer": self.user}

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

    def test_list_behind_authentication(self):
        """ Test review listing endpoint requires authentication. """
        # Given
        url = reverse("review-list")

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(JSONWebTokenAuthentication, "authenticate_credentials")
    @patch("rest_framework_jwt.authentication.jwt_decode_handler")
    @patch.object(JSONWebTokenAuthentication, "get_jwt_value")
    def test_list(self, jwt_value_mock, jwt_decode_mock, jwt_cred_mock):
        """
        Test review listing works as expected (only show reviews for user).

        """
        # setUp (Creating additional user and it's reviews)
        another_user = User.objects.create_superuser(
            'anothersuperuser@example.com',
            email='anothersuperuser@example.com',
            password='anothersuperuser')
        mixer.cycle(2).blend(models.Review, reviewer=another_user)

        # Given
        url = reverse("review-list")
        mixer.cycle(3).blend(models.Review, reviewer=self.user)

        # When
        jwt_value_mock.return_value = True
        jwt_decode_mock.return_value = True
        jwt_cred_mock.return_value = self.user
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_detail_behind_authentication(self):
        """ Test review detail endpoint requires authentication. """
        # Given
        url = reverse("review-list")

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(JSONWebTokenAuthentication, "authenticate_credentials")
    @patch("rest_framework_jwt.authentication.jwt_decode_handler")
    @patch.object(JSONWebTokenAuthentication, "get_jwt_value")
    def test_detail_alien(self,
                          jwt_value_mock, jwt_decode_mock, jwt_cred_mock):
        """
        Test review detail works as expected:

            Don't show review for another user.

        """
        # setUp (creating a different user)
        another_user = User.objects.create_superuser(
            'anothersuperuser@example.com',
            email='anothersuperuser@example.com',
            password='anothersuperuser')

        # Given
        review = mixer.blend(models.Review, reviewer=another_user)
        url = reverse("review-detail", args=[review.id])

        # When
        jwt_value_mock.return_value = True
        jwt_decode_mock.return_value = True
        jwt_cred_mock.return_value = self.user
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(JSONWebTokenAuthentication, "authenticate_credentials")
    @patch("rest_framework_jwt.authentication.jwt_decode_handler")
    @patch.object(JSONWebTokenAuthentication, "get_jwt_value")
    def test_detail(self, jwt_value_mock, jwt_decode_mock, jwt_cred_mock):
        """
        Test review detail works as expected:

            Show review for user.

        """
        # Given
        review = models.Review.objects.create(**self.object_create_data)
        url = reverse("review-detail", args=[review.id])

        # When
        jwt_value_mock.return_value = True
        jwt_decode_mock.return_value = True
        jwt_cred_mock.return_value = self.user
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), review.id)
        self.assertEqual(response.data.get("company"), self.company.id)
        self.assertEqual(response.data.get("reviewer"), self.user.id)

    @patch.object(JSONWebTokenAuthentication, "authenticate_credentials")
    @patch("rest_framework_jwt.authentication.jwt_decode_handler")
    @patch.object(JSONWebTokenAuthentication, "get_jwt_value")
    def test_detail_nested(self,
                           jwt_value_mock, jwt_decode_mock, jwt_cred_mock):
        """
        Test review detail works as expected:

            Show review for user (with detailed data for company/reviewer).

        """
        # Given
        review = models.Review.objects.create(**self.object_create_data)
        url = reverse("review-detail", args=[review.id])

        # When
        jwt_value_mock.return_value = True
        jwt_decode_mock.return_value = True
        jwt_cred_mock.return_value = self.user
        response = self.client.get(url, {"nested": True})

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), review.id)
        self.assertEqual(response.data.get("company").get("id"),
                         self.company.id)
        self.assertEqual(response.data.get("reviewer").get("id"),
                         self.user.id)

    def test_update_behind_authentication(self):
        """ Test review updating endpoint requires authentication. """
        # Given
        review = models.Review.objects.create(**self.object_create_data)
        url = reverse("review-detail", args=[review.id])

        # When
        response = self.client.put(url, self.create_data, format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(JSONWebTokenAuthentication, "authenticate_credentials")
    @patch("rest_framework_jwt.authentication.jwt_decode_handler")
    @patch.object(JSONWebTokenAuthentication, "get_jwt_value")
    def test_update(self, jwt_value_mock, jwt_decode_mock, jwt_cred_mock):
        """ Test review updating is not allowed. """
        # Given
        review = models.Review.objects.create(**self.object_create_data)
        url = reverse("review-detail", args=[review.id])

        # When
        jwt_value_mock.return_value = True
        jwt_decode_mock.return_value = True
        jwt_cred_mock.return_value = self.user
        response = self.client.put(url, self.create_data, format="json")

        # Then
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_destroy_behind_authentication(self):
        """ Test review destroying endpoint requires authentication. """
        # Given
        review = models.Review.objects.create(**self.object_create_data)
        url = reverse("review-detail", args=[review.id])

        # When
        response = self.client.put(url, format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(JSONWebTokenAuthentication, "authenticate_credentials")
    @patch("rest_framework_jwt.authentication.jwt_decode_handler")
    @patch.object(JSONWebTokenAuthentication, "get_jwt_value")
    def test_destroy(self, jwt_value_mock, jwt_decode_mock, jwt_cred_mock):
        """ Test review destruction is not allowed. """
        # Given
        review = models.Review.objects.create(**self.object_create_data)
        url = reverse("review-detail", args=[review.id])

        # When
        jwt_value_mock.return_value = True
        jwt_decode_mock.return_value = True
        jwt_cred_mock.return_value = self.user
        response = self.client.put(url, format="json")

        # Then
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
