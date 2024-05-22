from django.contrib import admin
from api.challenges.models import Challenge, ChallengeStep


admin.site.register(Challenge)
admin.site.register(ChallengeStep)
