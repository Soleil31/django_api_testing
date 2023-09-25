from django.urls import path
from .views import LessonListWithStatusView

urlpatterns = [
    path('lessons/', LessonListWithStatusView.as_view(), name='lesson-list-with-status'),
]