from django.contrib import admin
from .models import Expert, ExpertSkill, Review

admin.site.register(Expert)
admin.site.register(ExpertSkill)
admin.site.register(Review)