from django.shortcuts import render
from rest_framework import generics
from .models import Lesson
from .serializers import LessonWithStatusSerializer

class LessonListWithStatusView(generics.ListAPIView):
    serializer_class = LessonWithStatusSerializer

    def get_queryset(self):
        user = self.request.user
        lessons = Lesson.objects.filter(products__access__user=user)
        return lessons
