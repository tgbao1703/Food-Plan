from django.contrib import admin
from .models import Place, PlaceHotMark, PlaceMedia, Review, ReviewMedia, UserPresence, UserReputationStats

admin.site.register(UserReputationStats)
admin.site.register(UserPresence)
admin.site.register(Place)
admin.site.register(Review)
admin.site.register(ReviewMedia)
admin.site.register(PlaceMedia)
admin.site.register(PlaceHotMark)
