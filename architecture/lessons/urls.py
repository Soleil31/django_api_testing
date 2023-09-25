from django.urls import path
from .views import LessonListWithStatusView, LessonDetailByProductView

urlpatterns = [
    path('lessons/', LessonListWithStatusView.as_view(), name='lesson-list-with-status'),
    path('products/<int:product_id>/lessons/detail/', LessonDetailByProductView.as_view(), name='lesson-detail-by-product')
]