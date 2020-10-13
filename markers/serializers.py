from rest_framework import serializers

from authentication.models import Profile
from markers.models import GenericMarker, ExtraActivityMarker, StudyGroupMarker, ConstructionMarker, EventMarker, Marker


class MarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = '__all__'
        read_only_fields = ['id']


class GenericMarkerSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        if obj.profile is not None:
            return {
                'id': Profile.objects.get(id=obj.profile.id).id,
                'name': Profile.objects.get(id=obj.profile.id).name,
            }
        else:
            return None

    class Meta:
        model = GenericMarker
        fields = "__all__"
        read_only_fields = ['id']


class EventMarkerSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        if obj.profile is not None:
            return {
                'id': Profile.objects.get(id=obj.profile.id).id,
                'name': Profile.objects.get(id=obj.profile.id).name,
            }
        else:
            return None

    class Meta:
        model = EventMarker
        fields = '__all__'
        read_only_fields = ['id']


class ConstructionMarkerSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        if obj.profile is not None:
            return {
                'id': Profile.objects.get(id=obj.profile.id).id,
                'name': Profile.objects.get(id=obj.profile.id).name,
            }
        else:
            return None

    class Meta:
        model = ConstructionMarker
        fields = '__all__'
        read_only_fields = ['id']


class StudyGroupMarkerSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        if obj.profile is not None:
            return {
                'id': Profile.objects.get(id=obj.profile.id).id,
                'name': Profile.objects.get(id=obj.profile.id).name,
            }
        else:
            return None

    class Meta:
        model = StudyGroupMarker
        fields = '__all__'
        read_only_fields = ['id']


class ExtraActivityMarkerSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        if obj.profile is not None:
            return {
                'id': Profile.objects.get(id=obj.profile.id).id,
                'name': Profile.objects.get(id=obj.profile.id).name,
            }
        else:
            return None

    class Meta:
        model = ExtraActivityMarker
        fields = '__all__'
        read_only_fields = ['id']