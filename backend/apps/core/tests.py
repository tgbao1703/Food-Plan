from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Place, Review, UserReputationStats


class CoreApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass12345')
        self.place = Place.objects.create(
            name='Pho 24',
            address='HCMC',
            latitude=10.7769,
            longitude=106.7009,
            created_by=self.user,
            is_public=True,
        )

    def test_health_endpoint(self):
        response = self.client.get('/api/v1/health')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')

    def test_create_review_requires_auth(self):
        response = self.client.post('/api/v1/reviews', {'place': self.place.id, 'star': 5, 'content': 'Great'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_review_updates_user_stats(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/reviews', {'place': self.place.id, 'star': 5, 'content': 'Great'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        stats = UserReputationStats.objects.get(user=self.user)
        self.assertEqual(stats.total_reviews, 1)
        self.assertEqual(stats.gold_stars, 1)
        self.assertEqual(stats.comet_stars, 0)

    def test_route_validation(self):
        response = self.client.post('/api/v1/routes', {'origin': {'lat': 100, 'lng': 1}, 'destination': {'lat': 10, 'lng': 106}, 'mode': 'driving'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_place_detail_returns_public_place(self):
        response = self.client.get(f'/api/v1/places/{self.place.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Pho 24')
