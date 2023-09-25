from django.urls import path
from .views import LessonListWithStatusView, LessonDetailByProductView, ProductStatsView

urlpatterns = [
    path('lessons/', LessonListWithStatusView.as_view(), name='lesson-list-with-status'),
    path('products/<int:product_id>/lessons/detail/', LessonDetailByProductView.as_view(), name='lesson-detail-by-product'),
    path('product-stats/', ProductStatsView.as_view(), name='product-stats'),
]