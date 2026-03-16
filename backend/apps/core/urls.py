from django.urls import path

from .views import (
    HealthView,
    LeaderboardUsersView,
    PlaceDetailView,
    PlaceHotMarkCreateView,
    PlaceListCreateView,
    PlaceMediaView,
    PlaceReviewsView,
    ReviewCreateView,
    ReviewMediaCreateView,
    RouteView,
    UserDetailView,
    UserReviewsView,
)

urlpatterns = [
    path('health', HealthView.as_view(), name='health'),
    path('places', PlaceListCreateView.as_view(), name='places-list-create'),
    path('places/<int:pk>', PlaceDetailView.as_view(), name='places-detail'),
    path('places/<int:pk>/reviews', PlaceReviewsView.as_view(), name='places-reviews'),
    path('places/<int:pk>/media', PlaceMediaView.as_view(), name='places-media'),
    path('places/<int:pk>/hot-marks', PlaceHotMarkCreateView.as_view(), name='places-hot-marks'),
    path('reviews', ReviewCreateView.as_view(), name='reviews-create'),
    path('reviews/<int:pk>/media', ReviewMediaCreateView.as_view(), name='reviews-media-create'),
    path('leaderboard/users', LeaderboardUsersView.as_view(), name='leaderboard-users'),
    path('users/<int:pk>', UserDetailView.as_view(), name='users-detail'),
    path('users/<int:pk>/reviews', UserReviewsView.as_view(), name='users-reviews'),
    path('routes', RouteView.as_view(), name='routes'),
]
