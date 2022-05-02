from django.urls import path

from core.views import NavView

urlpatterns = [
    path('/nav', NavView.as_view())
]