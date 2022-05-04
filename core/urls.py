from django.urls import path

from core.views import TopicView

urlpatterns = [
    path('/topic', TopicView.as_view()),
]