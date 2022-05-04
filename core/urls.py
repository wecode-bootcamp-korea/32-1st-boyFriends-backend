from django.urls import path

from core.views import MainCategoryView

urlpatterns = [
    path('/nav', MainCategoryView.as_view())
]