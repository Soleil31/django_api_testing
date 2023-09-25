from rest_framework import serializers
from .models import Lesson, LessonStatus

#first api
class LessonStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonStatus
        fields = ['status', 'watched_time', 'watched_at']

class LessonWithStatusSerializer(serializers.ModelSerializer):
    status = LessonStatusSerializer(many=True, read_only=True, source='lessonstatus_set')

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_link', 'duration', 'status']

#second api
class LessonDetailSerializer(serializers.ModelSerializer):
    status = LessonStatusSerializer(source='get_lesson_status', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_link', 'duration', 'status']