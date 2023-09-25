from rest_framework import serializers
from .models import Lesson, LessonStatus

class LessonStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonStatus
        fields = ['status', 'watched_time']

class LessonWithStatusSerializer(serializers.ModelSerializer):
    status = LessonStatusSerializer(many=True, read_only=True, source='lessonstatus_set')

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_link', 'duration', 'status']