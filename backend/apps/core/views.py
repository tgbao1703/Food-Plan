from math import radians, cos, sin, asin, sqrt

from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Place, PlaceHotMark, PlaceMedia, Review, UserReputationStats
from .serializers import (
    CreateReviewSerializer,
    PlaceMediaSerializer,
    PlaceSerializer,
    ReviewMediaSerializer,
    ReviewSerializer,
    RouteRequestSerializer,
    UserCompactSerializer,
    UserReputationSerializer,
)


def _recalculate_user_stats(user: User) -> None:
    stats, _ = UserReputationStats.objects.get_or_create(user=user)
    reviews = Review.objects.filter(user=user)
    stats.total_reviews = reviews.count()
    stats.gold_stars = reviews.filter(star__gte=4).count()
    stats.comet_stars = reviews.filter(star__lte=2).count()
    stats.gold_comet_ratio = (stats.gold_stars + 1) / (stats.comet_stars + 1)
    stats.save()


class HealthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'status': 'ok'})


class PlaceListCreateView(generics.ListCreateAPIView):
    serializer_class = PlaceSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return Place.objects.filter(is_public=True).annotate(hot_marks_count=Count('hot_marks')).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PlaceDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Place.objects.filter(is_public=True).annotate(hot_marks_count=Count('hot_marks'))
    serializer_class = PlaceSerializer


class PlaceReviewsView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(place_id=self.kwargs['pk']).select_related('user').prefetch_related('media').order_by('-created_at')


class PlaceMediaView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PlaceMediaSerializer

    def get_queryset(self):
        return PlaceMedia.objects.filter(place_id=self.kwargs['pk']).order_by('-id')


class ReviewCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateReviewSerializer

    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)
        _recalculate_user_stats(review.user)


class ReviewMediaCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewMediaSerializer

    def create(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs['pk'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(review=review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LeaderboardUsersView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserReputationSerializer

    def get_queryset(self):
        return UserReputationStats.objects.select_related('user').order_by('-gold_comet_ratio', '-gold_stars', '-total_reviews')


class UserDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        stats, _ = UserReputationStats.objects.get_or_create(user=user)
        return Response({'user': UserCompactSerializer(user).data, 'stats': UserReputationSerializer(stats).data})


class UserReviewsView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user_id=self.kwargs['pk']).select_related('user').prefetch_related('media').order_by('-created_at')


class PlaceHotMarkCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk: int):
        place = get_object_or_404(Place, pk=pk)
        mark, created = PlaceHotMark.objects.get_or_create(user=request.user, place=place)
        return Response({'id': mark.id, 'created': created}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class RouteView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RouteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        origin = payload['origin']
        destination = payload['destination']
        mode = payload['mode']

        distance_km = haversine_km(origin['lat'], origin['lng'], destination['lat'], destination['lng'])
        speed = {'driving': 35, 'bike': 18, 'walking': 5}[mode]
        eta_min = int((distance_km / speed) * 60)

        return Response(
            {
                'routes': [
                    {'name': 'fastest', 'distance_km': round(distance_km, 2), 'eta_min': max(1, eta_min)},
                    {
                        'name': 'shortest',
                        'distance_km': round(distance_km * 0.95, 2),
                        'eta_min': max(1, int(eta_min * 1.15)),
                    },
                ]
            }
        )


def haversine_km(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371 * c
