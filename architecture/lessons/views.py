from django.shortcuts import render
from rest_framework import generics
from .models import Lesson
from .serializers import LessonWithStatusSerializer, LessonDetailSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class LessonListWithStatusView(generics.ListAPIView):
    serializer_class = LessonWithStatusSerializer

    def get_queryset(self):
        user = self.request.user
        lessons = Lesson.objects.filter(products__access__user=user)
        return lessons

class LessonDetailByProductView(generics.ListAPIView):
    serializer_class = LessonDetailSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']  #ID продукта из URL
        lessons = Lesson.objects.filter(products__access__user=user, products__id=product_id)
        return lessons