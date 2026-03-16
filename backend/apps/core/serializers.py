from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Place, PlaceHotMark, PlaceMedia, Review, ReviewMedia, UserReputationStats


class UserCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserReputationSerializer(serializers.ModelSerializer):
    user = UserCompactSerializer()

    class Meta:
        model = UserReputationStats
        fields = ['user', 'total_reviews', 'gold_stars', 'comet_stars', 'gold_comet_ratio']


class PlaceMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceMedia
        fields = ['id', 'media_url', 'metadata']


class PlaceSerializer(serializers.ModelSerializer):
    hot_marks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Place
        fields = [
            'id',
            'name',
            'address',
            'latitude',
            'longitude',
            'tags',
            'opening_hours',
            'created_by',
            'is_public',
            'created_at',
            'hot_marks_count',
        ]
        read_only_fields = ['created_by', 'created_at', 'hot_marks_count']

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError('latitude must be between -90 and 90')
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError('longitude must be between -180 and 180')
        return value


class ReviewMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewMedia
        fields = ['id', 'media_url', 'media_type', 'metadata']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserCompactSerializer(read_only=True)
    media = ReviewMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'place', 'star', 'content', 'created_at', 'media']
        read_only_fields = ['user', 'created_at']


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['place', 'star', 'content']

    def validate_star(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('star must be between 1 and 5')
        return value


class HotMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceHotMark
        fields = ['id', 'place', 'created_at']
        read_only_fields = ['created_at']


class RouteRequestSerializer(serializers.Serializer):
    origin = serializers.DictField()
    destination = serializers.DictField()
    mode = serializers.ChoiceField(choices=['driving', 'bike', 'walking'], default='driving')

    def _validate_point(self, name: str, value: dict) -> dict:
        if 'lat' not in value or 'lng' not in value:
            raise serializers.ValidationError({name: 'lat and lng are required'})

        lat = value['lat']
        lng = value['lng']
        if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
            raise serializers.ValidationError({name: 'lat and lng must be numbers'})
        if lat < -90 or lat > 90:
            raise serializers.ValidationError({name: 'lat out of range'})
        if lng < -180 or lng > 180:
            raise serializers.ValidationError({name: 'lng out of range'})
        return value

    def validate_origin(self, value):
        return self._validate_point('origin', value)

    def validate_destination(self, value):
        return self._validate_point('destination', value)
