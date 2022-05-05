from django.urls import path

from products.views import TopicView


urlpatterns = [
    path('/topic', TopicView.as_view()),
]