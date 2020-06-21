from django.contrib import admin

from authentication.models import Profile
from markers.models import GenericMarker, EventMarker, ConstructionMarker, StudyGroupMarker, ExtraActivityMarker

admin.site.register(GenericMarker)
admin.site.register(EventMarker)
admin.site.register(ConstructionMarker)
admin.site.register(StudyGroupMarker)
admin.site.register(ExtraActivityMarker)
admin.site.register(Profile)