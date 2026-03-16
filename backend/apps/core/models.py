from django.contrib.auth.models import User
from django.db import models


class UserReputationStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reputation')
    total_reviews = models.PositiveIntegerField(default=0)
    gold_stars = models.PositiveIntegerField(default=0)
    comet_stars = models.PositiveIntegerField(default=0)
    gold_comet_ratio = models.FloatField(default=1.0)

    def recalculate(self) -> None:
        self.gold_comet_ratio = (self.gold_stars + 1) / (self.comet_stars + 1)
        self.save(update_fields=['gold_comet_ratio'])


class UserPresence(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)


class Place(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tags = models.CharField(max_length=255, blank=True)
    opening_hours = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_places')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='reviews')
    star = models.PositiveSmallIntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ReviewMedia(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='media')
    media_url = models.URLField()
    media_type = models.CharField(max_length=20, default='image')
    metadata = models.JSONField(default=dict, blank=True)


class PlaceMedia(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='media')
    media_url = models.URLField()
    source_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    metadata = models.JSONField(default=dict, blank=True)


class PlaceHotMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='hot_marks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place')
