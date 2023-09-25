from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Lesson, LessonStatus, Product, Access
from .serializers import LessonWithStatusSerializer, LessonDetailSerializer, ProductStatsSerializer


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
    
class ProductStatsView(generics.ListAPIView):
    serializer_class = ProductStatsSerializer

    def get_queryset(self):
        return Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = []
        
        for product in queryset:
            stats = product.get_product_stats()
            serialized_data.append({
                'id': product.id,
                'name': product.name,
                'stats': stats,
            })

        return Response(serialized_data)