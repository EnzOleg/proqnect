from django.contrib import admin
from .models import Expert, ExpertSkill, ExpertReview

admin.site.register(Expert)
admin.site.register(ExpertSkill)
admin.site.register(ExpertReview)