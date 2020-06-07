from rest_framework import serializers

from markers.models import GenericMarker, ExtraActivityMarker, StudyGroupMarker, ConstructionMarker, EventMarker


class GenericMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericMarker
        fields = '__all__'
        read_only_fields = ['id']

class EventMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMarker
        fields = '__all__'
        read_only_fields = ['id']

class ConstructionMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionMarker
        fields = '__all__'
        read_only_fields = ['id']

class StudyGroupMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroupMarker
        fields = '__all__'
        read_only_fields = ['id']

class ExtraActivityMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraActivityMarker
        fields = '__all__'
        read_only_fields = ['id']